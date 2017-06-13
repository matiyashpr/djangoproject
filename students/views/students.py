

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib import messages

from django.forms import ModelForm
from django.views.generic import UpdateView, DeleteView
from django.utils.translation import ugettext as _

from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required

from crispy_forms.helper import FormHelper
from crispy_forms.layout import Submit
from crispy_forms.bootstrap import FormActions

from django.shortcuts import get_object_or_404, redirect, render
from .forms import StudentUpdateForm
from ..util import paginate, get_current_group

from io import BytesIO
from PIL import Image
from datetime import datetime

from ..models.students import Student
from ..models.groups import Group

import logging

def students_list(request):
    current_group = get_current_group(request)
    if current_group:
        students = Student.objects.filter(student_group=current_group)
    else:
        students = Student.objects.all()
        
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
        
    context = paginate(students, 5, request, {}, var_name='students')
    
    return render (request, 'students/students_list.html', context)
           

@login_required            
def students_add(request, *args, **kwargs):
    
        #if form posted:
    if request.method == "POST":
        if request.POST.get('add_button') is not None:

            errors = {}
            
            data = {'middle_name': request.POST.get('middle_name'), 'notes': request.POST.get('notes')}
            
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = _(u"First Name field is required")
            else:
                data['first_name'] = first_name
             
            last_name = request.POST.get('last_name', '').strip()
            if not last_name :
                errors['last_name'] = _(u"Last name field is required")
            else:
                data['last_name'] = last_name
                
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = _(u"Birthdate field is required")
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = _(u"Enter currently format (Example 1998.02.26)")
                else:
                    data['birthday'] = birthday
                
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = _(u"Ticket number is required")
            else:
                data['ticket'] = ticket
                
            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = _(u"Select the group for student")
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = _(u"Choose a specific group")
                else:
                    data['student_group'] = groups[0]
            
            photo = request.FILES.get('photo')
            if not photo: 
                errors['photo'] = _(u'Choose a photo')
            else:
                FORMAT_PHOTO = ('jpg', 'jpeg', 'png', 'bmp')
                SIZE_PHOTO = 10
                SIZE_THUMNAIL = (500,500)
                if photo.size > SIZE_PHOTO*1024*1000:
                    errors['photo'] = "".join([_("Photo size should not exceed "), str(SIZE_PHOTO), _("megabyte")])
                    photo = None


                if photo:
                    try:
                        img = Image.open(photo)
                        img.thumbnail(SIZE_THUMNAIL, Image.ANTIALIAS)
                        thumb_io = BytesIO()
                        _format = photo.content_type.split('/')[1]
                        img.save(thumb_io, _format)
                        _file = thumb_io
                        field_name = photo.field_name
                        name = "".join([datetime.now().strftime("%Y-%m-%d %H-%M-%S"),".",_format])
                        content_type = photo.content_type
                        im = InMemoryUploadedFile(_file, field_name, name, content_type, size=None, charset=None)
                        data['photo'] = im
                    except IOError: 
                        errors['photo'] = _("This should be a picture, such as file format %s") % ", ".join(FORMAT_PHOTO)
                
            if not errors:
                student = Student(**data)
                student.save()
            
                messages.success(request, _(u'Student %s %s added successfully!') %(data['last_name'], data['first_name']))
                return HttpResponseRedirect(reverse('home'))
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})
        
        elif request.POST.get('cancel_button') is not None: messages.warning(request, _(u'Adding student canceled!'))
        return HttpResponseRedirect(reverse('home'))
            
    else:
          return render(request,'students/students_add.html',{'groups': Group.objects.all().order_by('title')})

        

                
def student_update(request, some_id):
    stud = get_object_or_404(Student, id=some_id)
    form = StudentUpdateForm(request.POST or None, instance=stud)
    if request.method == 'POST':
        if form.is_valid():
            # do_something
            form.save()
            messages.success(self.request, _(u"Student - {}, was successfully updated!".format(stud.some_name)))
            return redirect(reverse('home'))
        return render(request, 'students/students_edit.html', {'form': form, 'student': stud}) 
    

class EditStudentView(UpdateView):
    model = Student
    template_name = 'students/students_edit.html'
    form_class = StudentUpdateForm

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentUpdateView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        messages.success(self.request, _(u"Student {} updated successfully!".format(self.object.last_name)))
        return reverse('home')




class StudentDeleteView(DeleteView):
    model = Student
    template_name = 'students/students_confirm_delete.html'

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StudentDeleteView, self).dispatch(*args, **kwargs)

    def get_success_url(self):
        return _(u'%s?status_message=Student successfully deleted!') % reverse('home')

