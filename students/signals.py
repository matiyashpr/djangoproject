# -*- coding: utf-8 -*-
import logging
import random

from django.utils.crypto import get_random_string
from django.db.models.signals import post_save, post_delete
from django.dispatch import receiver
from django.contrib.auth.models import User
from django.utils.text import slugify
from models.students import Student
from django.core.files import File

@receiver(post_save, sender=Student)
def log_student_updated_added_event(sender, **kwargs):
    logger = logging.getLogger(__name__)
    
    student = kwargs['instance']
    if kwargs ['created']:
        logger.info("Student added: %s %s (ID: %d)", student.first_name, student.last_name, student.id)
    else:
        logger.info("Student updated: %s %s (ID: %d)", student.first_name, student.last_name, student.id)
        
@receiver(post_delete, sender=Student)
def log_student_delete_event(sender, **kwargs):
    logger = logging.getLogger(__name__)
    
    student = kwargs['instance']
    logger.info("Student deleted: %s %s (ID: %d)", student.first_name, student.last_name, student.id)
        
@receiver(post_save, sender=Student)
def create_user(sender, instance, created, **kwargs):
    if created:
        password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        username = get_random_string(10)
        User.objects.create(username=username, password=password)
        file = open("us_pas.txt","w")
        file.write( username)
        file.write( password)
        file.close()
            