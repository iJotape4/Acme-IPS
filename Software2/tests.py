from django.test import TestCase, SimpleTestCase
from django.shortcuts import reverse

class Test1(SimpleTestCase):

    def test_principal(self):
        response = self.client.get('principal/')
        self.assertEquals(response.status_code , 404)

    def test_url_principal(self):
        response = self.client.get(reverse('principal'))
        self.assertEquals(response.status_code, 200)
    
    def test_correct_template_princi(self):
        response = self.client.get(reverse('principal'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, 'principalPage.html')


    def test_agendar_correo(self):
        response = self.client.get('correo/')
        self.assertEquals(response.status_code , 404)

    def test_url_agendar_correo(self):
        response = self.client.get(reverse('correo'))
        self.assertEquals(response.status_code, 200)
    
    def test_correct_template_correo(self):
        response = self.client.get(reverse('correo'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'./regisCorreo.html','plantilla.html')

    