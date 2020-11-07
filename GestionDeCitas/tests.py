from django.test import TestCase, SimpleTestCase
from django.shortcuts import reverse

class Test3(TestCase):
    def test_agendarCita(self):
        response = self.client.get('/agendar_cita/')
        self.assertEquals(response.status_code , 200)

    def test_url_agendarCita(self):
        response = self.client.get(reverse('agendar'))
        self.assertEquals(response.status_code, 200)
        
    def test_correct_template_agendarCita(self):
        response = self.client.get(reverse('agendar'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response, "agendamiento_Citas.html")