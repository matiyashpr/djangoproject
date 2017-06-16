# -*- coding: utf-8 -*-
import logging
import random
import codecs
import io
import shutil

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
def create_user(sender, created, **kwargs):
    student = kwargs['instance']
    if created:
        password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        user, created = User.objects.get_or_create(username= get_random_string(10))
        if created:
            user.set_password(password) # This line will hash the password
            user.save()
            student.user_field = user
            upas = student.first_name, ' ', student.last_name, ' ', ' username - ', user.username, ' password - ', password
            import codecs
            file = io.open("us_pas.txt", "a", encoding="utf-8")
            file.write(unicode (upas))
            file.close()        
             
        
        
"""

@receiver(post_save, sender=Student)
def create_user(sender, created, **kwargs):
    student = kwargs['instance']
    if created:
        password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        user, created = User.objects.get_or_create(username= get_random_string(10))
        if created:
            user.set_password(password) # This line will hash the password

            user.save()            
            upas = student.first_name, ' ', student.last_name, ' ', ' username - ', user.username, ' password - ', password
            import codecs
            file = io.open("us_pas.txt", "a", encoding="utf-8")
            file.write(unicode (upas))
            file.close()
        
       
        
        
        
        
        
        
        
        
        

        password = User.objects.make_random_password(length=10, allowed_chars='abcdefghjkmnpqrstuvwxyzABCDEFGHJKLMNPQRSTUVWXYZ23456789')
        username = get_random_string(10)
        User.objects.create(username=username, password=password)
        file = open("us_pas.txt","w")
        file.write( username)
        file.write( password)
        file.close()
"""        