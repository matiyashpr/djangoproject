# -*- coding: utf-8 -*-
from django.contrib import admin
from django.core.urlresolvers import reverse
from django.forms import ModelForm, ValidationError
from django.utils.translation import ugettext_lazy as _

from models.students import Student
from models.groups import Group
from models.monthjournal import MonthJournal
from models.exam import Exam
from models.exam_result import Exam_result
from functools import partial

class StudentFormAdmin(ModelForm):

    def clean_student_group(self):
        groups = Group.objects.filter(leader=self.instance)
        if len(groups) > 0 and self.cleaned_data['student_group'] != groups[0]:
            raise ValidationError(_(u'The student is leader of another group', code='invalid'))
        return self.cleaned_data['student_group']

class StudentAdmin(admin.ModelAdmin):
    list_display = ['last_name', 'first_name', 'ticket', 'student_group']
    list_display_links = ['last_name', 'first_name']
    list_editable = ['student_group']
    ordering = ['last_name']
    list_filter = ['student_group']
    list_per_page = 10
    search_fields = ['last_name', 'first_name', 'middle_name', 'ticket',
                     'notes']
    
    def view_on_site(self, obj):
        return reverse('students_edit', kwargs={'pk': obj.id})
    
class GroupFormAdmin(ModelForm):

    def __init__(self, *args, **kwargs):
        super(GroupFormAdmin, self).__init__(*args, **kwargs)
        # filter students for current group
        self.fields['leader'].queryset = self.instance.student_set.all().order_by('last_name')

    def clean_leader(self):
        leader = self.cleaned_data['leader']
        if not leader or leader.student_group_id == self.instance:
            return leader
        else:
            raise ValidationError(u'Студент належить до іншої групи.', code='invalid')

#@admin.register(Group)            
class GroupAdmin(admin.ModelAdmin):
    list_display = ['title', 'leader']
    list_display_links = ['title']
    list_editable = ['leader']
    ordering = ['title']
    list_filter = ['title']
    list_per_page = 10
    search_fields = ['title', 'leader',
                     'notes']
    
    def get_form(self, request, obj=None, **kwargs):
        kwargs['formfield_callback'] = partial(self.formfield_for_dbfield, request=request, obj=obj)
        return super(GroupAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name != "leader":
            kwargs.pop('obj', None)
        return super(GroupAdmin, self).formfield_for_dbfield(db_field, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        group = kwargs.pop('obj', None)
        if db_field.name == 'leader' and group:
            kwargs['queryset'] = Student.objects.filter(student_group_id=group.id)
            return super(GroupAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)

    def view_on_site(self, obj):
        return reverse('groups_edit', kwargs={'pk': obj.id})
    


# Register your models here.

admin.site.register(Student, StudentAdmin)
admin.site.register(Group, GroupAdmin)
admin.site.register(MonthJournal)
admin.site.register(Exam)
admin.site.register(Exam_result)
