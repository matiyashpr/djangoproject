from django.template import Template, Context
from django.test import TestCase
from django.core.paginator import Paginator

class TemplateTagTests(TestCase):
    
    def test_str2int(self):
        out = Template(
            "{% load str2int %}"
            "{% if 36 == '36' |str2int %}"
            "it works"
            "{% endif %}"
        ).render(Context({}))
        
        self.assertIn("it works", out)
        