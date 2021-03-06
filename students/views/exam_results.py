# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views.generic import CreateView, UpdateView, DeleteView
from django.forms import ModelForm
from django.contrib import messages

from crispy_forms.bootstrap import AppendedText, PrependedText
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, HTML, Div
from crispy_forms.bootstrap import FormActions, AppendedText
from crispy_forms.layout import Layout
from django.utils.translation import ugettext as _

from ..models.students import Student
from ..models.exam_result import Exam_result
from ..util import paginate, get_current_group

def exam_results(request):
    
    user = request.user
    user_field = Student.user_field    
    current_group = get_current_group(request)
    
    if current_group:
        exams = Exam_result.objects.filter(forexam__exam_group=current_group)
    else: 
        if Student.objects.filter(user_field=user):
            one_student = Student.objects.get(user_field=user)
            one_student_id = one_student.id
            exams = Exam_result.objects.filter(student_name_id=one_student_id)
        else:
            exams = Exam_result.objects.all()
        
    order_by = request.GET.get('order_by', '')
    if order_by in ('forexam__date', 'forexam__teacher', 'forexam__title', 'forexam__exam_group__title', 'student_name__last_name', 'evaluation'):
        exams = exams.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            exams = exams.reverse()

    paginator = Paginator(exams, 3)
    page = request.GET.get('page')
    try:
        exams = paginator.page(page)
    except PageNotAnInteger:
        exams = paginator.page(1)
    except EmptyPage:
        exams = paginator.page(paginator.num_pages)

    return render(request, 'students/exam_results.html', {'exams': exams})

class ExamResultCreateForm(ModelForm):
    class Meta:
        model = Exam_result
    def __init__(self, *args, **kwargs):
        super(ExamResultCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        self.helper.form_action = reverse('exam_result_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper['date'].wrap(AppendedText, '<i class="glyphicon glyphicon-calendar"></i>')

        self.helper.layout.append(HTML(
            _(u'<div class="form-group"><label class="col-sm-2 control-label"></label><div class="controls col-sm-10">\
        <input class="btn btn-primary" type="submit" value="Save" name="add_button" />\
        <a class="btn btn-link" name="cancel_button" href="{% url "exams" %}?status_message= "Add/Edit result canceled" > Cancel </a>\
        </div></div>')))

class ExamResultCreateView(CreateView):
    model = Exam_result
    template_name = 'students/exam_result_edit.html'
    form_class = ExamResultCreateForm
    
    def get_success_url(self):
        messages.success(self.request, _(u'Exam result %s added successfully!') % self.object)
        return reverse('exam_results')
    
    
    
class ExamResultUpdateForm(ExamResultCreateForm):

    def __init__(self, *args, **kwargs):
        super(ExamResultUpdateForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('exam_result_edit', kwargs = {'pk': kwargs['instance'].id})

class ExamResultUpdateView(UpdateView):
    model = Exam_result
    template_name = 'students/exam_result_edit.html'
    form_class = ExamResultUpdateForm

    def get_success_url(self):
        messages.success(self.request, _(u'Exam result %s saved successfully!') % self.object)
        return reverse('exam_results')

class ExamResultDeleteView(DeleteView):
    model = Exam_result
    template_name = 'students/exams_result_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, _(u'Exam result %s delete successfully!') % self.object)
        return reverse('exam_results')