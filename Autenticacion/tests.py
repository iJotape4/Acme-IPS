from django.test import TestCase, SimpleTestCase
from django.shortcuts import reverse

class Test2(SimpleTestCase):
    def test_login(self):
        response = self.client.get('login/')
        self.assertEquals(response.status_code , 404)

    def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        
    def test_correct_template_login(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'login.html')