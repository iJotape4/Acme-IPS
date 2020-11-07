from django.test import TestCase, SimpleTestCase
from django.shortcuts import reverse

# Create your tests here.

    ######

class Test2(SimpleTestCase):

    def test_login(self):
        response = self.client.get('/login/')
        self.assertEquals(response.status_code , 200)

    def test_login_url(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        
    def test_correct_template_login(self):
        response = self.client.get(reverse('login'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'login.html')

    #####

    def test_menu_paciente(self):
        response = self.client.get('/menu_Paciente/')
        self.assertEquals(response.status_code , 200)

    def test_menu_paciente_url(self):
        response = self.client.get(reverse('memu_paciente'))
        self.assertEquals(response.status_code, 200)
        
    def test_correct_template_menu_paciente(self):
        response = self.client.get(reverse('memu_paciente'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'login.html', 'plantilla.html')

    ######

    def test_registro(self):
        response = self.client.get('/registro/')
        self.assertEquals(response.status_code , 200)

    def test_registro_url(self):
        response = self.client.get(reverse('registro'))
        self.assertEquals(response.status_code, 200)
        
    def test_correct_template_registro(self):
        response = self.client.get(reverse('registro'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'registro.html')

    #####
    def test_recuperar_contra(self):
        response = self.client.get('/recuperarContraseña/')
        self.assertEquals(response.status_code , 200)

    def test_recuperar_contra_url(self):
        response = self.client.get(reverse('recuperar_Contra'))
        self.assertEquals(response.status_code, 200)
        
    def test_correct_template_recuperar_contra(self):
        response = self.client.get(reverse('recuperar_Contra'))
        self.assertEquals(response.status_code, 200)
        self.assertTemplateUsed(response,'recuperarContra.html')