from django.db import models
from decimal import Decimal


class TransactionType(models.Model):
    """
    Transaction Type model
    """
    N_INPUT = 'Entrada'
    N_OUTPUT = 'Saída'
    NATURE_CHOICES = (
        (N_INPUT, N_INPUT),
        (N_OUTPUT, N_OUTPUT),
    )

    S_POSITIVE = '+'
    S_NEGATIVE = '-'
    SIGN_CHOICES = (
        (S_POSITIVE, S_POSITIVE),
        (S_NEGATIVE, S_NEGATIVE),
    )

    t_type = models.IntegerField(unique=True, verbose_name='Tipo')
    description = models.CharField(max_length=60, verbose_name='Descrição')
    nature = models.CharField(
        max_length=7, choices=NATURE_CHOICES, verbose_name='Natureza')
    sign = models.CharField(
        max_length=1, choices=SIGN_CHOICES, verbose_name='Sinal')

    def __str__(self):
        """Default string representation of the object

        Returns:
            string: default string representation of the object
        """
        return str(self.t_type)


class Store(models.Model):
    """
    Store model
    """
    name = models.CharField(max_length=19, verbose_name='Nome da loja')
    owner = models.CharField(max_length=14, verbose_name='Dono da loja')

    class Meta:
        unique_together = ('name', 'owner')

    def get_total_amount(self):
        """Calculate the store's total balance

        Returns:
            Decimal: total balance
        """
        transactions = self.transactions.values_list('amount', 't_type__sign')
        total = Decimal('0.00')
        for t in transactions:
            total += t[0] if t[1] == TransactionType.S_POSITIVE else -t[0]
        return total

    def __str__(self):
        """Default string representation of the object

        Returns:
            string: default string representation of the object
        """
        return self.name


class Transaction(models.Model):
    """
    Transaction model
    """
    store = models.ForeignKey(
        Store, on_delete=models.PROTECT, related_name='transactions', verbose_name='Loja')
    t_type = models.ForeignKey(
        TransactionType, on_delete=models.PROTECT, related_name='transactions', verbose_name='Tipo')
    date = models.DateField(verbose_name='Data')
    amount = models.DecimalField(
        decimal_places=2, max_digits=8, verbose_name='Valor')
    cpf = models.CharField(max_length=11, verbose_name='CPF')
    card = models.CharField(max_length=12, verbose_name='Cartão')
    time = models.TimeField(verbose_name='Hora')

    def __str__(self):
        """Default string representation of the object

        Returns:
            string: default string representation of the object
        """
        return str(self.pk)
