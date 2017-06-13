# -*- coding: utf-8 -*-

from django.db import models

class Exam(models.Model):

    class Meta(object):
        verbose_name = u"Іспит"
        verbose_name_plural = u"Іспити"
        unique_together = (('title', 'exam_group'), ('date', 'teacher'), ('date', 'exam_group'))

    title = models.CharField(
        max_length=128,
        blank=False,
        verbose_name=u"Назва предмету")

    date = models.DateTimeField(
        blank=False,
        verbose_name=u"Дата і час проведення",
        null=True)

    teacher = models.CharField(
        max_length=128,
        blank=False,
        verbose_name=u"Ім'я викладача")

    exam_group = models.ForeignKey('Group',
        verbose_name=u"Група",
        blank=False,
        null=True)

    def __unicode__(self):
        return u"%s %s" % (self.exam_group.title, self.title)
    