from rest_framework import routers

from .views import FileUploadView, StoreList, CustomAuthToken, TransactionsList, Register, UserInfo, TypeTransactionsList
from django.urls import re_path, path, include

app_name = 'api'
router = routers.DefaultRouter()
router.register('stores', StoreList, basename='Stores')
router.register('transactions', TransactionsList, basename='Transactions')
router.register('type-transactions', TypeTransactionsList, basename='TypeTransactionsList')

urlpatterns = [

    path('api-token-auth/', CustomAuthToken.as_view()),
    path('register/', Register.as_view()),
    path('user_info/', UserInfo.as_view()),
    path('', include(router.urls)),
    re_path(r'^upload/(?P<filename>[^/]+)$',
            FileUploadView.as_view(), name='upload')
]
