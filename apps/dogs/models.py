# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.
class Rate(models.Model):
    rate = models.IntegerField()
    date = models.DateTimeField()
