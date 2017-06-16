# -*- coding: utf-8 -*-
from django.db import models
from django.utils.translation import ugettext_lazy as _

class Exam_result(models.Model):

    class Meta(object):
        verbose_name = _(u"Exam result")
        verbose_name_plural = _(u"Exam results")
        unique_together = ('forexam', 'student_name')

    forexam = models.ForeignKey('Exam',
        verbose_name=_(u"Exam"),
        blank=False,
        null=True)

    student_name = models.ForeignKey('Student',
        verbose_name=_(u"Student"),
        blank=False,
        null=True)

    evaluation = models.PositiveSmallIntegerField(
        verbose_name=_(u"Score"))

    def __unicode__(self):
       return u"%s %s %s" % (self.student_name, self.forexam.title, self.forexam.id)

