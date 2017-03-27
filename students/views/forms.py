# -*- coding: utf-8 -*-

from django.forms import ModelForm
from ..models.students import Student


class StudentUpdateForm(ModelForm):
    class Meta():
        model = Student
        fields = '__all__'