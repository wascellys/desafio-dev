from rest_framework import serializers
from .models import Store, Transaction, TransactionType


class TransactionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Transaction
        fields = ('id','date', 'cpf', 'amount', 'card', 'time', 't_type','store')
        depth = 2


class StoreSerializer(serializers.ModelSerializer):
    transactions = TransactionSerializer(many=True)
    total_amount = serializers.SerializerMethodField(read_only=True)

    def get_total_amount(self, obj):
        return obj.get_total_amount()

    class Meta:
        model = Store
        fields = ('id','name', 'owner', 'transactions', 'total_amount')


class TransactionTypeSerializer(serializers.ModelSerializer):
    class Meta:
        model = TransactionType
        fields = '__all__'