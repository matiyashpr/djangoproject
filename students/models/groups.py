

from __future__ import unicode_literals

from django.db import models

from django.forms import ModelForm
from django.utils.translation import ugettext_lazy as _
# Create your models here.

       
class Group(models.Model):
    
    class Meta(object):
        verbose_name = _(u"Group")
        verbose_name_plural = _(u"Groups")
        
    title = models.CharField(
        max_length=256,
        blank=False,
        verbose_name=_(u"Name"))
    
    leader = models.OneToOneField(
        'Student',
        verbose_name=_(u"Leader"),
        blank=True,
        null=True,
        on_delete=models.SET_NULL)
    
    notes = models.TextField(
        blank=True,
        verbose_name=_(u"Notes"))
    
    def __unicode__(self):
        if self.leader:
            return u"%s (%s %s)" % (self.title, self.leader.first_name,
                                    self.leader.last_name)
        else:
            return u"%s" % (self.title,)
        
                                  
