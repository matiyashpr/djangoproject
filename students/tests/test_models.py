from django.test import TestCase

from students.models.students import Student

class StudentModelTests(TestCase):
    
    def test_unicode(self):
        student = Student(first_name='Demo', last_name='Student')
        self.assertEqual(unicode(student), u'Demo Student')