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




# Views for Groups

        
def groups_list(request):
    groups = (
            {'id' : 1,
            'id_group' : u'44-ПЗ',
            'leader' : u'Матіяш Василь'},
        
            {'id' : 2,
             'id_group' : u'43-ПЗ',
             'leader' : u'Савечко Тарас'},
        
            {'id' : 3,
             'id_group' : u'45-КІ',
             'leader' : u'Надія Надієчка'},
            )
    return render(request, 'students/groups_list.html', {'groups': groups})

def groups_add(request):
	return HttpResponse('<h1>Group Add Form</h1>')

def groups_edit(request, gid):
	return HttpResponse('<h1>Edit Group %s</h1>' % gid)

def groups_delete(request, gid):
	return HttpResponse('<h1>Delete Group %s</h1>' % gid)

# Create your views here.
