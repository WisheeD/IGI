from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.models import User
from Main.models import *


class BuyRealtyViewTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(username='testuser', password='12345')
        self.realty = Realty.objects.create(name='Test Realty', price=100000, owner=self.user, area=120, address='Test Address', realty_type='house', image='aboba.png')

    def test_buy_realty_view(self):
        self.client.login(username='testuser', password='12345')
        response = self.client.post(reverse('buy_realty', kwargs={'pk': self.realty.pk}))
        self.assertEqual(response.status_code, 302)
        self.realty.refresh_from_db()
        self.assertEqual(self.realty.status, 'available')

    def test_home_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
        response = self.client.post(url, {'username': 'testuser', 'password': '12345'})
        self.assertEqual(response.status_code, 200)

    def test_logout_view(self):
        url = reverse('logout')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 302)

    def test_create_review_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('create_review')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_vacancy_view(self):
        url = reverse('list_vacancy')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_news_view(self):
        url = reverse('list_news')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_review_view(self):
        url = reverse('list_review')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_vacancy_details_view(self):
        vacancy = Vacancy.objects.create(title='Test Vacancy', description='Test Description')
        url = reverse('vacancy_detail', kwargs={'pk': vacancy.pk})
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_company_view(self):
        url = reverse('company')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_question_view(self):
        url = reverse('list_question')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_employee_view(self):
        url = reverse('list_employee')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_realty_view(self):
        url = reverse('home')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_list_purchases_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('list_purchased')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)

    def test_coupon_list_view(self):
        self.client.login(username='testuser', password='12345')
        url = reverse('list_coupon')
        response = self.client.get(url)
        self.assertEqual(response.status_code, 200)
