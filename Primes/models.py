from django.db import models
from django.contrib.postgres.fields import ArrayField


class Primes(models.Model):
    number = models.IntegerField(default=0)
    primes = ArrayField(models.IntegerField(default=0),default=[])

    def __str__(self):
        return "{1}: {2}".format(self.number, self.primes)
