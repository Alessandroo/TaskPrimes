# Задача. На django. По запросу GET /<basedir>/get_prime/<value> вернуть JSON объект вида
# {
# value: primes[],
# status: status
# }
#
# короче primes это разложение value на простые множители, STATUS - код возврата. можно вернуть success, processing или error.
# Само разложение:
# смотрим, считали ли данное число ранее, если считали, возвращаем ответ и success
# если нет, запускаем поток и считаем, если завершился нормально возвращаем success, иначе error
# если сейчас работает поток, который обрабатывает данное число, возвращаем только статус processing
import time
from django.http import HttpResponse
from django.http import HttpResponseRedirect
from django.shortcuts import render_to_response, render
import re
import threading
import json
from Primes.models import Primes


class AsyncResult(threading.Thread):
    def __init__(self, func, args):
        threading.Thread.__init__(self)
        self.func = func
        self.args = args
        self.result = None
        self.status = None

    def run(self):
        print('Я в run')
        try:
            self.result = self.func(*self.args)
            self.status = 'success'
            p = Primes(number=self.args[0], primes=self.result)
            p.save()
        except Exception as e:
            self.result = []
            self.status = 'error'

    def is_ready(self):
        return not self.isAlive()

    def get_value(self):
        if self.status != 'error':
            if not self.is_ready():
                self.status = 'processing'
                answer = json.dumps({'status': self.status}, separators=(',', ':'))
                self.join()
            else:
                answer = json.dumps({'value': self.result, 'status': self.status}, separators=(',', ':'))
        else:
            answer = json.dumps({'value': self.result, 'status': self.status}, separators=(',', ':'))
        return HttpResponse(answer)


def get_primes(number):
    answer = []
    d = 2
    while d * d <= number:
        if number % d == 0:
            answer.append(d)
            number //= d
        else:
            d += 1
    if number > 1:
        answer.append(number)
    return answer


def index(request):
    return render_to_response('index.html', {})


def browser(request):
    print('I here')
    ua = request.get_full_path(force_append_slash=True)
    url_pattern = '/get_prime/(?P<value>[0-9]+)/'
    m = re.match(url_pattern, ua)
    if m is not None:
        numbers = int(m.group('value'))
        try:
            inf = Primes.objects.get(number=numbers)
        except Primes.DoesNotExist:
            inf = None
        if inf is not None:
            answer = json.dumps({'value': inf.primes, 'status': 'success'}, separators=(',', ':'))
            return HttpResponse(answer)
        else:
            b = AsyncResult(get_primes, (numbers,))
            b.setDaemon(True)
            b.start()
            return b.get_value()
    else:
        return render_to_response('index.html')
