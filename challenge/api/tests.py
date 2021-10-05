from django.contrib.auth.models import User
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient

from .models import Store, TransactionType
from django.test import TestCase
from random import randint
from django.utils import timezone
from decimal import Decimal


class StoreTestCase(TestCase):

    def setUp(self):
        username = 'usuario'
        password = 'teste123'
        self.user = User.objects.create_user(
            username=username, password=password
        )

        # User authentication
        self.client = APIClient()
        self.client.login(username=username, password=password)

        self.store = Store.objects.create(
            name='Store Test',
            owner='Edy Ferreira',
        )

        TransactionType.objects.create(
            t_type=0,
            description='Boleto',
            nature='Saída',
            sign='-',
        )
        TransactionType.objects.create(
            t_type=1,
            description='Crédito',
            nature='Entrada',
            sign='+',
        )
        self.total_amount = Decimal('0.00')
        for _ in range(10):
            rand = randint(0, 100)
            t_type = rand % 2
            self.total_amount += rand if t_type else -rand
            dt = timezone.now()
            self.store.transactions.create(
                t_type=TransactionType.objects.get(t_type=t_type),
                date=dt.date(),
                time=dt.time(),
                cpf='00000000000',
                card='0000****0000',
                amount=Decimal(str(rand)),
            )

    def test_store_total_amount(self):
        total_amount = self.store.get_total_amount()
        self.assertEqual(total_amount, self.total_amount)


