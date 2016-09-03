import threading


global PERENT


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
    print(answer)

def paran():
    print(PERENT)

if __name__ == '__main__':
    t = threading.Thread(target=get_primes, args=(25**12+1,))
    t.start()
    PERENT = t
    paran()