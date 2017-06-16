# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView, DeleteView
from functools import partial
from django.core.exceptions import ValidationError
from django.utils.translation import ugettext as _
from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from ..models.groups import Group
from ..util import paginate


def groups_list(request):
    groups = Group.objects.all()
    
    order_by = request.GET.get('order_by', '')
    if order_by in ('title',):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()

    context = paginate(groups, 3, request, {}, var_name='groups')
    return render(request, 'students/groups_list.html', context)

class GroupForm(ModelForm):
    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        super(GroupForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        if kwargs['instance'] is None:
            add_form = True
        else:
            add_form = False

        if add_form:
            self.helper.form_action = reverse('groups_add')
        else:
            self.helper.form_action = reverse('groups_edit',
                kwargs={'pk': kwargs['instance'].id})
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        self.helper.help_text_inline = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'  
        
        if add_form:
            submit = Submit('add_button', _(u'Add'),
                css_class="btn btn-primary")
        else:
            submit = Submit('save_button', _(u'Save'),
                css_class="btn btn-primary")
        self.helper.layout[-1] = FormActions(
            submit,
            Submit('cancel_button', _(u'Cancel'), css_class="btn btn-link"),
        )
        
    def get_form(self, request, obj=None, **kwargs):
        kwargs['formfield_callback'] = partial(self.formfield_for_dbfield, request=request, obj=obj)
        return super(GroupAdmin, self).get_form(request, obj, **kwargs)

    def formfield_for_dbfield(self, db_field, **kwargs):
        if db_field.name != "leader":
            kwargs.pop('obj', None)
        return super(GroupForm, self).formfield_for_dbfield(db_field, **kwargs)

    def formfield_for_foreignkey(self, db_field, request, **kwargs):
        group = kwargs.pop('obj', None)
        if db_field.name == 'leader' and group:
            kwargs['queryset'] = Student.objects.filter(student_group_id=group.id)
        return super(GroupAdmin, self).formfield_for_foreignkey(db_field, request, **kwargs)
    
    def clean_leader(self):
        student_instance = self.cleaned_data.get('leader')
        if student_instance:
            if student_instance.student_group_id == self.instance.id:
                return student_instance
            else:
                self.add_error('leader', ValidationError (_(u'This student from other group.')))

class BaseGroupFormView(object):

    def get_success_url(self):
        return _(u'%s?status_message=Changes successfully saved!') % reverse('groups')

    def post(self, request, *args, **kwargs):
        if request.POST.get('cancel_button'):
            return HttpResponseRedirect(reverse('groups') +_( u'?status_message=Changes canceled.'))
        else:
            return super(BaseGroupFormView, self).post(request, *args, **kwargs)

class GroupAddView(BaseGroupFormView, CreateView):
    model = Group
    form_class = GroupForm
    template_name = 'students/groups_form.html'

class GroupUpdateView(BaseGroupFormView, UpdateView):
    model = Group
    form_class = GroupForm
    template_name = 'students/groups_form.html'

class GroupDeleteView(BaseGroupFormView, DeleteView):
    model = Group
    template_name = 'students/groups_confirm_delete.html'