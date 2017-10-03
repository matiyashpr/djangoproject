from datetime import datetime

from django.test import TestCase, Client
from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.contrib.auth.models import Permission


from students.models.groups import Group
from students.models.students import Student

class TestStudentList(TestCase):
    
    def setUp(self):
        group1, created = Group.objects.get_or_create(title='KN-113')
        group2, created = Group.objects.get_or_create(title='KN-112')
        
        Student.objects.get_or_create(
            first_name='Vasil',
            last_name='Matiyash',
            birthday=datetime.today(),
            ticket='4213',
            student_group=group1)
    
        Student.objects.get_or_create(
                first_name='Lubomyr',
                last_name='Prystanskii',
                birthday=datetime.today(),
                ticket='2143',
                student_group=group2)

        Student.objects.get_or_create(
                first_name='Igor',
                last_name='Mazur',
                birthday=datetime.today(),
                ticket='4213',
                student_group=group2)

        Student.objects.get_or_create(
                first_name='Tanya',
                last_name='Shcherbyna',
                birthday=datetime.today(),
                ticket='5234',
                student_group=group2)
        
        self.client = Client()        
        permission = Permission.objects.get(name='Can add user')
        self.user = User.objects.create_user('test_user', password='test_user')        
        self.user.user_permissions.add(permission)
        
        self.url = reverse('home')
        
    def test_students_list(self):
        
        self.client.login(username='test_user', password='test_user')       
        response = self.client.get(reverse('home'))        
        self.assertEqual(response.status_code, 200)        
        self.assertIn('Vasil', response.content)        
        self.assertIn(reverse('students_edit', kwargs={'pk': Student.objects.all()[0].id}), response.content)        
        self.assertEqual(len(response.context['students']), 4)
        
    def test_current_group(self):
        self.client.login(username='test_user', password='test_user')
        group = Group.objects.filter(title="KN-113")[0]
        self.client.cookies['current_group'] = group.id
        
        response = self.client.get(self.url)
        
        self.assertEqual(len(response.context['students']), 1)
        
    def test_order_by(self):
        self.client.login(username='test_user', password='test_user')
        response = self.client.get(self.url, {'order_by': 'last_name'})
        
        students = response.context['students']
        self.assertEqual(students[0].last_name, 'Matiyash')
        self.assertEqual(students[1].last_name, 'Mazur')
        self.assertEqual(students[2].last_name, 'Prystanskii')
        self.assertEqual(students[3].last_name, 'Shcherbyna')
        