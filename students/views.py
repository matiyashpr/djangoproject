# -*- coding: utf-8 -*-
from django.shortcuts import render
from django.http import HttpResponse

def students_add(request):
    return render(request, 'students/students_add.html',
            {})


# Create your views here.
