# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView, DeleteView
from django.utils.translation import ugettext as _

from crispy_forms.bootstrap import AppendedText, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Div
from crispy_forms.bootstrap import FormActions, AppendedText
from crispy_forms.layout import Layout

from ..models.students import Student
from ..models.exam import Exam
from ..util import paginate, get_current_group

class ExamCreateForm(ModelForm):
    class Meta:
        model = Exam
    def __init__(self, *args, **kwargs):
        super(ExamCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_action = reverse('exams_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-3'
                
        self.helper['date'].wrap(AppendedText, '<i class=" glyphicon glyphicon-calendar"></i>')

        self.helper.layout.append(HTML(
            _(u'<div class="form-group"><label class="col-sm-2 control-label"></label><div class="controls col-sm-10">\
        <input class="btn btn-primary" type="submit" value="Save" name="add_button" />\
        <a class="btn btn-link" name="cancel_button" href="{% url "exams" %}?status_message="Add/Edit exam canceled">Cancel</a>\
        </div></div>')))

class ExamUpdateForm(ExamCreateForm):

    def __init__(self, *args, **kwargs):
        super(ExamUpdateForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('exams_edit', kwargs = {'pk': kwargs['instance'].id})

class ExamCreateView(CreateView):
    model = Exam
    template_name = 'students/exams_edit.html'
    form_class = ExamCreateForm

    def get_success_url(self):
        messages.success(self.request, _(u'Exam %s added successfully!') % self.object)
        return reverse('exams')

class ExamUpdateView(UpdateView):
    model = Exam
    template_name = 'students/exams_edit.html'
    form_class = ExamUpdateForm

    def get_success_url(self):
        messages.success(self.request, _(u'Exam %s saved successfully!') % self.object)
        return reverse('exams')

class ExamDeleteView(DeleteView):
    model = Exam
    template_name = 'students/exams_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, _(u'Exam %s delete successfully!') % self.object)
        return reverse('exams')

def exams_list(request, *args, **kwargs):
    
    user = request.user
    user_field = Student.user_field    
    current_group = get_current_group(request)
    
    if current_group:
        exams = Exam.objects.filter(exam_group=current_group)
    else: 
        if Student.objects.filter(user_field=user):
            one_student = Student.objects.get(user_field=user)
            one_student_group = one_student.student_group
            exams = Exam.objects.filter(exam_group=one_student_group)
        else:
            exams = Exam.objects.all()

    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'date', 'teacher', 'exam_group'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()

    context = paginate(exams, 3, request, {}, var_name='exams')
    return render(request, 'students/exams.html', context)