from django.contrib import admin
from .models import TransactionType, Transaction, Store

admin.site.register(TransactionType)
admin.site.register(Transaction)
admin.site.register(Store)
