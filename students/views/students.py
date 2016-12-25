# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.core.urlresolvers import reverse
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.core.files.uploadedfile import InMemoryUploadedFile
from django.contrib import messages

from io import BytesIO
from PIL import Image
from datetime import datetime

from ..models.students import Student
from ..models.groups import Group


def students_list(request):
    students = Student.objects.all()
    
    if request.get_full_path() == "/":
        #redirect request.GET on its copy(deep copy) which I will amend
        request.GET = request.GET.copy()
        #assign 'order_by' value 'last_name' 
        request.GET.__setitem__('order_by', 'last_name')
    
    order_by = request.GET.get('order_by', '')
    if order_by in ('last_name', 'first_name', 'ticket'):
        students = students.order_by(order_by)
        if request.GET.get('reverse', '') == '1':
            students = students.reverse()
            
    paginator = Paginator(students, 3)
    page = request.GET.get('page')
    try:
        students = paginator.page(page)
    except PageNotAnInteger:
        students = paginator.page (1)
    except EmptyPage:
        students = paginator.page(paginator.num_pages)
    
    
    return render(request, 'students/students_list.html',
                  {'students': students})
           

            
def students_add(request):
    
        #Якщо форма була запощена:
    if request.method == "POST":
        if request.POST.get('add_button') is not None:

            errors = {}
            
            data = {'middle_name': request.POST.get('middle_name'), 'notes': request.POST.get('notes')}
            
            first_name = request.POST.get('first_name', '').strip()
            if not first_name:
                errors['first_name'] = u"Ім'я є обов'язковим"
            else:
                data['first_name'] = first_name
             
            last_name = request.POST.get('last_name', '').strip()
            if not last_name :
                errors['last_name'] = u"Прізвище є обов'язковим"
            else:
                data['last_name'] = last_name
                
            birthday = request.POST.get('birthday', '').strip()
            if not birthday:
                errors['birthday'] = u"Дата народження є обов'язковою"
            else:
                try:
                    datetime.strptime(birthday, '%Y-%m-%d')
                except Exception:
                    errors['birthday'] = u"Введіть коректний формат дати (напр. 1998-03-26)"
                else:
                    data['birthday'] = birthday
                
            ticket = request.POST.get('ticket', '').strip()
            if not ticket:
                errors['ticket'] = u"Номер білета є обов'язковим"
            else:
                data['ticket'] = ticket
                
            student_group = request.POST.get('student_group', '').strip()
            if not student_group:
                errors['student_group'] = u"Оберіть групу для студента"
            else:
                groups = Group.objects.filter(pk=student_group)
                if len(groups) != 1:
                    errors['student_group'] = u"Оберіть конкретну групу"
                else:
                    data['student_group'] = groups[0]
            
            photo = request.FILES.get('photo')
            if not photo: 
                errors['photo'] = u'Виберіть фото'
            else:
                FORMAT_PHOTO = ('jpg', 'jpeg', 'png', 'bmp')
                SIZE_PHOTO = 10
                SIZE_THUMNAIL = (500,500)
                if photo.size > SIZE_PHOTO*1024*1000:
                    errors['photo'] = "".join(["Розмір фото не повинен перевищувати ", str(SIZE_PHOTO), "мегабайт"])
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
                        errors['photo'] = "Це повинно бути фото, наприклад файли з розширенням %s" % ", ".join(FORMAT_PHOTO)
                
            if not errors:
                student = Student(**data)
                student.save()
            
                messages.success(request, u'Студента %s %s успішно додано!' %(data['last_name'], data['first_name']))
                return HttpResponseRedirect(reverse('home'))
            else:
                # render form with errors and previous user input
                return render(request, 'students/students_add.html',
                              {'groups': Group.objects.all().order_by('title'),
                               'errors': errors})
        
        elif request.POST.get('cancel_button') is not None:
            messages.warning(request, u'Додавання студента скасовано!')
            return HttpResponseRedirect(reverse('home'))
            
    else:
          return render(request,'students/students_add.html',{'groups': Group.objects.all().order_by('title')})

                
 

def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)
