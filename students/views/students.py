# -*- coding: utf-8 -*-

from django.shortcuts import render
from django.http import HttpResponse


def students_list(request):
	students = (
        {'id' : 1,
         'first_name' : u'Олег',
         'last_name' : u'Курилас',
         'ticket' : 2123,
         'image' : 'img/Kurilas.jpg'},
      
      {'id' : 2,
       'first_name' : u'Вячеслав',
       'last_name' : u'Дрофа',
       'ticket' : 1147,
       'image' : 'img/Drofa.jpg'},
     
      {'id' : 3,
       'first_name' : u'Любомир',
       'last_name' : u'Пристанський',
       'ticket' : 3422,
       'image' : 'img/Pristansky.jpg'},
                )  
        return render(request, 'students/students_list.html', {'students': students})
        
                  

def students_add(request):
	return HttpResponse('<h1>Student Add Form</h1>')

def students_edit(request, sid):
	return HttpResponse('<h1>Edit Student %s</h1>' % sid)

def students_delete(request, sid):
	return HttpResponse('<h1>Delete Student %s</h1>' % sid)
