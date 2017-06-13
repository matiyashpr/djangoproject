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

from ..models.exam_result import Exam_result
from ..util import paginate, get_current_group

def exam_results(request):
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
        # If page is not an integer, deliver first page.
        exams = paginator.page(1)
    except EmptyPage:
        # If page is out of range (e.g. 9999), deliver last page of results.
        exams = paginator.page(paginator.num_pages)

    return render(request, 'students/exam_results.html', {'exams': exams})

class ExamResultCreateForm(ModelForm):
    class Meta:
        model = Exam_result
    def __init__(self, *args, **kwargs):
        super(ExamResultCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('exam_result_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        self.helper['date'].wrap(AppendedText, '<i class="glyphicon glyphicon-calendar"></i>')

        # add buttons
        self.helper.layout.append(HTML(
            u'<div class="form-group"><label class="col-sm-2 control-label"></label><div class="controls col-sm-10">\
        <input class="btn btn-primary" type="submit" value="Зберегти" name="add_button" />\
        <a class="btn btn-link" name="cancel_button" href="{% url "exams" %}?status_message=Додавання/редагування іспиту скасовано!">Скасувати</a>\
        </div></div>'))

class ExamResultCreateView(CreateView):
    model = Exam_result
    template_name = 'students/exams_edit.html'
    form_class = ExamResultCreateForm

    def get_success_url(self):
        return render(request, 'students/exam_results.html', {'exams': exams})