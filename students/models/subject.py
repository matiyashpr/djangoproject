# -*- coding: utf-8 -*-

from django.db import models
from django.contrib.auth.models import User
from django.utils.translation import ugettext_lazy as _

class Subject(models.Model):

    class Meta(object):
        verbose_name = _(u"Subject")
        verbose_name_plural = _(u"Subjects")      

    title = models.CharField(
        max_length=128,
        blank=False,
        verbose_name=_(u"Name of subject"))

    teacher = models.CharField(
        max_length=128,
        blank=False,
        verbose_name=_(u"Professor name"))

    teacher_field = models.OneToOneField(User, on_delete=models.CASCADE, related_name="t_user", null=True, blank=False)

    def __unicode__(self):
        return u"%s" % ( self.title)
    