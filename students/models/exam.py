# -*- coding: utf-8 -*-

from django.db import models
from django.utils.translation import ugettext_lazy as _

class Exam(models.Model):

    class Meta(object):
        verbose_name = _(u"Exam")
        verbose_name_plural = _(u"Exams")
        unique_together = (('title', 'exam_group'), ('date', 'teacher'), ('date', 'exam_group'))

    title = models.ForeignKey('Subject',
        verbose_name=_(u"Subject name"),
        blank=True,
        null=False,
        )

    date = models.DateTimeField(
        blank=False,
        verbose_name=_(u"Date and time"),
        null=True)

    teacher = models.CharField(
        max_length=128,
        blank=False,
        verbose_name=_(u"Professor"))

    exam_group = models.ForeignKey('Group',
        verbose_name=_(u"Group"),
        blank=False,
        null=True)

    def __unicode__(self):
        return u"%s %s" % (self.exam_group.title, self.title)
    