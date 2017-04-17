# -*- coding: utf-8 -*-
from django.db import models
from django.db.models.signals import post_save
from django.contrib.auth.models import User

class Document(models.Model):
    docfile = models.FileField(upload_to='documents/%Y/%m/%d')
    owner = models.ForeignKey('Drinker', on_delete=models.CASCADE, default=None, blank=True, null=True)
    shared = models.BooleanField(default=False)
    fx = models.BooleanField(default=False)
    description = models.CharField(max_length=100, blank=True, null=True )



class Drinker(models.Model):
        user            = models.OneToOneField(User)
        birthday        = models.DateField()
        name            = models.CharField(max_length=100)

        def __unicode__(self):
                return self.name

                
