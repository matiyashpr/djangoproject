# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.db.models.signals import post_save
from django.utils.translation import ugettext_lazy as _
from django.contrib.auth.models import User
from django.dispatch import receiver

class Student(models.Model):
        
        class Meta(object):
            verbose_name = _(u"Student")
            verbose_name_plural = _(u"Students")
        
        first_name = models.CharField(
            max_length=256,
            blank=False,
            verbose_name=_(u"First Name"))
        
        last_name = models.CharField(
            max_length=256,
            blank=False,
            verbose_name=_(u"Last Name"))
        
        middle_name = models.CharField(
            max_length=256,
            blank=True,
            verbose_name=_(u"Middle Name"),
            default='')
        
        birthday = models.DateField(
            blank=False,
            verbose_name=_(u"Birthdate"),
            null=True)
        
        photo = models.ImageField(
            blank=True,
            verbose_name=_(u"Photo"),
            null=True)
        
        ticket = models.CharField(
            max_length=256,
            blank=False,
            verbose_name=_(u"Ticket"))
        
        notes = models.TextField(
            blank=True,
            verbose_name=_(u"Notes"))
        
        student_group = models.ForeignKey('Group',
            verbose_name=_(u"Group"),
            blank=False,
            null=True,
            on_delete=models.PROTECT)
        
        user_field = models.OneToOneField(User, on_delete=models.CASCADE, related_name="user", null=True, blank=False)
               
        def __unicode__(self):
            return u"%s %s" % (self.first_name, self.last_name)  
          
      
