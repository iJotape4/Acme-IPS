from django.test import TestCase, SimpleTestCase
from django.shortcuts import reverse

class Test4(TestCase):

    def test_recuperar_citas_del_dia(self):
        response = self.client.get('/citas_del_dia/')
        self.assertEquals(response.status_code , 200)

    def test_citas_del_dia_url(self):
        response = self.client.get(reverse('citasDia'))
        self.assertEquals(response.status_code, 200)
        
    def test_correct_template_citas_del_dia(self):
        response = self.client.get(reverse('citasDia'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'./citas_del_dia.html')
