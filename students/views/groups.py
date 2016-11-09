# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse


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
