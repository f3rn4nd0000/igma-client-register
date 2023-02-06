from django.db import models
from datetime import datetime
from django.utils import timezone
# Create your models here.
class PersonModel(models.Model):
    name = models.CharField(max_length=40, blank=False, default='')
    cpf = models.CharField(max_length=11,blank=False, default='')
    birthdate = models.DateField(max_length=10, default=timezone.now, )