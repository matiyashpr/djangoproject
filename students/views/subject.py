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
#from django.contrib.auth.models import User

from ..models.students import Student
from ..models.subject import Subject
from ..util import paginate, get_current_group

class SubjectCreateForm(ModelForm):
    class Meta:
        model = Subject
        exclude = ['teacher_field']
    def __init__(self, *args, **kwargs):
        super(SubjectCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('subjects_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-3'

        # add buttons
        self.helper.layout.append(HTML(
            _(u'<div class="form-group"><label class="col-sm-2 control-label"></label><div class="controls col-sm-10">\
    <input class="btn btn-primary" type="submit" value="Save" name="add_button" />\
    <a class="btn btn-link" name="cancel_button" href="{% url "subjects" %}?status_message=Add/Edit exam canceled>Cancel</a>\
    </div></div>')))
        
class SubjectUpdateForm(SubjectCreateForm):

    def __init__(self, *args, **kwargs):
        super(SubjectUpdateForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('subjects_edit', kwargs = {'pk': kwargs['instance'].id})

class SubjectCreateView(CreateView):
    model = Subject
    template_name = 'students/subject_edit.html'
    form_class = SubjectCreateForm

    def get_success_url(self):
        messages.success(self.request, _(u'Subject %s added successfully!') % self.object)
        return reverse('subjects')

class SubjectUpdateView(UpdateView):
    model = Subject
    template_name = 'students/subject_edit.html'
    form_class = SubjectUpdateForm

    def get_success_url(self):
        messages.success(self.request, _(u'Subject %s saved successfully!') % self.object)
        return reverse('subjects')

class SubjectDeleteView(DeleteView):
    model = Subject
    template_name = 'students/subjects_confirm_delete.html'

    def get_success_url(self):
        messages.success(self.request, _(u'Subject %s delete successfully!') % self.object)
        return reverse('subjects')
    
def subject_list(request, *args, **kwargs):

    subjects = Subject.objects.all()
    
    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'teacher'):
        subjects = subjects.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            subjects = subjects.reverse()

    context = paginate(subjects, 3, request, {}, var_name='subjects')
    return render(request, 'students/subjects.html', context)    