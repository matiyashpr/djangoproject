# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse


def journal(request):
    students = (
        {'id' : 1,
         'first_name' : u'Олег',
         'last_name' : u'Курилас'},
        
        {'id' : 2,
         'first_name' : u'Вячеслав',
         'last_name' : u'Дрофа'},
        
        {'id' : 3,
         'first_name' : u'Любомир',
         'last_name' : u'Пристанський'},
             )  
    return render(request, 'students/journal.html', {'students': students})