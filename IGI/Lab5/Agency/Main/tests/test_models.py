from django.test import TestCase
from Main.models import Deal, User, Realty


class DealModelTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create(username='testuser', password='<PASSWORD>', email='<EMAIL>')
        self.realty = Realty.objects.create(name='Test Realty', price=100000, owner=self.user, area=120, address='Test Address', realty_type='house')
        self.deal = Deal.objects.create(property=self.realty, client=self.user, deal_type='sale', amount=100000, status='pending')

    def test_deal_creation(self):
        self.assertEqual(self.deal.property, self.realty)
        self.assertEqual(self.deal.client, self.user)
        self.assertEqual(self.deal.amount, 100000)
        self.assertEqual(self.deal.status, 'pending')

    def test_realty_creation(self):
        self.assertEqual(self.realty.name, 'Test Realty')
        self.assertEqual(self.realty.price, 100000)
        self.assertEqual(self.realty.owner, self.user)

    def test_user_creation(self):
        self.assertEqual(self.user.username, 'testuser')
        self.assertEqual(self.user.email, '<EMAIL>')
        self.assertEqual(self.user.password, '<PASSWORD>')
