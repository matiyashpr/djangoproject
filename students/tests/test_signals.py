import logging

from django.utils.six import StringIO
from django.test import TestCase

from students.models.students import Student
from students import signals

class StudentSignalsTests(TestCase):
    def test_log_student_updated_added_event(self):
        out = StringIO()
        handler = logging.StreamHandler(out)
        logging.root.addHandler(handler)
        
        student = Student(first_name='Demo', last_name='Student')
        student.save()
        
        out.seek(0)
        self.assertEqual(out.readlines()[-1], 'Student added: Demo Student (ID: %d)\n' % student.id)
        
        student.ticker = '12345'
        student.save()
        out.seek(0)
        self.assertEqual(out.readlines()[-1], 'Student updated: Demo Student (ID: %d)\n' % student.id)
        
        logging.root.removeHandler(handler)
        
        