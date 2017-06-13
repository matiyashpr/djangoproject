# -*- coding: utf-8 -*-

from django.db import models

class Exam_result(models.Model):

    class Meta(object):
        verbose_name = u"Результат іспиту"
        verbose_name_plural = u"Результати іспитів"
        unique_together = ('forexam', 'student_name')

    forexam = models.ForeignKey('Exam',
        verbose_name=u"Іспит",
        blank=False,
        null=True)

    student_name = models.ForeignKey('Student',
        verbose_name=u"Студент",
        blank=False,
        null=True)

    evaluation = models.PositiveSmallIntegerField(
        verbose_name=u"Оцінка")

    def __unicode__(self):
       return u"%s %s %s" % (self.student_name, self.forexam.title, self.forexam.id)

