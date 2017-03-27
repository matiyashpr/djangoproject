# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.contrib import messages

from django.forms import ModelForm
from django.views.generic import CreateView, UpdateView, DeleteView

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit, Div, HTML
from crispy_forms.bootstrap import FormActions

from ..models.groups import Group

class GroupCreateForm(ModelForm):
    class Meta:
        model = Group

    def __init__(self, *args, **kwargs):
        super(GroupCreateForm, self).__init__(*args, **kwargs)

        self.helper = FormHelper(self)

        # set form tag attributes
        self.helper.form_action = reverse('groups_add')
        self.helper.form_method = 'POST'
        self.helper.form_class = 'form-horizontal'

        # set form field properties
        self.helper.help_text_inline = True
        self.helper.html5_required = True
        self.helper.label_class = 'col-sm-2 control-label'
        self.helper.field_class = 'col-sm-10'

        # add buttons
        self.helper.layout.append(FormActions(
            Div(css_class = self.helper.label_class),
            Submit('add_button', u'Зберегти', css_class="btn btn-primary"),
            HTML(u"<a class='btn btn-link' name='cancel_button' href='{% url 'groups' %}?status_message=Додавання/редагування групи скасовано!'>Скасувати</a>"),
        ))
        self.fields['leader'].queryset = self.fields['leader'].queryset.none()

class GroupUpdateForm(GroupCreateForm):

    def __init__(self, *args, **kwargs):
        super(GroupUpdateForm, self).__init__(*args, **kwargs)
        self.helper.form_action = reverse('group_edit', kwargs = {'pk': kwargs['instance'].id})
        self.fields['leader'].queryset = self.instance.student_set.all().order_by('last_name')

class GroupCreateView(CreateView):
    model = Group
    template_name = 'students/group_edit.html'
    form_class = GroupCreateForm

    def get_success_url(self):
        messages.info(self.request, u'Групу %s успішно додано!' % self.object.title)
        return reverse('groups')

class GroupUpdateView(UpdateView):
    model = Group
    template_name = 'students/group_edit.html'
    form_class = GroupUpdateForm

    def form_valid(self, form):
        leader = form.cleaned_data['leader']
        if not leader or leader.student_group_id == form.instance.id:
            return super(GroupUpdateView, self).form_valid(form)
        else:
            messages.error(self.request, u'Студент належить до іншої групи')
            return super(GroupUpdateView, self).form_invalid(form)

    def get_success_url(self):
        messages.info(self.request, u'Групу %s успішно збережено!' % self.object.title)
        return reverse('groups')


def groups_list(request):
    groups = Group.objects.all()
    
    if request.get_full_path() == "/":
        #redirect request.GET on its copy(deep copy) which I will amend
        request.GET = request.GET.copy()
        #assign 'order_by' value 'last_name' 
        request.GET.__setitem__('order_by', 'title')

    order_by = request.GET.get('order_by', '')
    if order_by in ('title', 'leader'):
        groups = groups.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            groups = groups.reverse()
    
    
    paginator = Paginator(groups, 3)
    page = request.GET.get('page')
    try:
        groups = paginator.page(page)
    except PageNotAnInteger:
            groups = paginator.page (1)
    except EmptyPage:
         groups = paginator.page(paginator.num_pages)
                
                
    return render(request, 'students/groups_list.html',
                 {'groups' : groups})

class GroupDeleteView(DeleteView):
    model = Group
    template_name = 'students/group_delete.html'

    def get_success_url(self):
        return u'%s?status_message=Групу успішно видалено!' % reverse('groups')
    
    def delete(self, request, *args, **kwargs):
        self.object = self.get_object()
        try:
            self.object.delete()
        except:
            return HttpResponseRedirect(u"%s?status_message=Не можливо видалити групу - скоріш за все в групі ще є студенти!" % reverse('groups'))
        else:
            return HttpResponseRedirect(self.get_success_url())
