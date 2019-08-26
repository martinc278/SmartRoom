from django.db import models

import datetime
from django.utils import timezone
from .settings import *

# Create your models here.
class Chair(models.Model):
    idc = models.CharField('chair ID', max_length=20, primary_key=True)
    ip = models.GenericIPAddressField('chair IP address', unique=True)

    def __str__(self):
        return (self.idc)


class Measure(models.Model):
    sensor_distance = models.CharField(max_length=20)
    sensor_temperature = models.CharField(max_length=20)
    date = models.DateTimeField()
    idc = models.ForeignKey(Chair, on_delete=models.CASCADE)

    def __str__(self):
        return ('{:<20} [{}]'.format(str(self.idc), str(self.date)))

    def was_measured_recently(self):
        return self.date >= timezone.now() - datetime.timedelta(minutes=MEASURES_PERSISTENCE)

    was_measured_recently.admin_order_field = 'date'
    was_measured_recently.boolean = True
    was_measured_recently.short_description = 'Measured recently?'
