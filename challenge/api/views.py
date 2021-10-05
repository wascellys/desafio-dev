from django.contrib.auth.models import User
from rest_framework.authentication import SessionAuthentication, TokenAuthentication
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.permissions import IsAuthenticated
from rest_framework.viewsets import ModelViewSet

from .models import TransactionType, Transaction, Store
from .serializers import StoreSerializer, TransactionSerializer, TransactionTypeSerializer
from django.db import transaction, IntegrityError
from .utils import CNABFile
from rest_framework.views import APIView
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.parsers import FileUploadParser


class CustomAuthToken(ObtainAuthToken):

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data,
                                           context={'request': request})
        serializer.is_valid(raise_exception=True)
        user = serializer.validated_data['user']
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        })


class FileUploadView(APIView):
    parser_classes = [FileUploadParser]

    def post(self, request, filename, format=None):
        """Import file

        Args:
            request (HttpRequest): request object
            filename (string): filename
            format (string, optional): request format. Defaults to None.

        Returns:
            Response: response object
        """

        file_obj = request.data[filename]
        cnab = CNABFile(file_obj)
        stores = cnab.stores
        with transaction.atomic():
            for s in stores:
                store, created = Store.objects.get_or_create(**s.get('store'))
                transactions = [
                    Transaction(store=store, t_type=TransactionType.objects.get(t_type=t.pop('t_type')), **t) for t in
                    s.get('transactions')
                ]
                store.transactions.bulk_create(transactions)

        return Response(status=201)


class Register(APIView):

    def post(self, request, format=None):

        try:
            with transaction.atomic():
                user = User.objects.create(username=request.data.get('username'), email=request.data.get('email'))
                user.set_password(request.data.get('password'))
                user.save()
                token, created = Token.objects.get_or_create(user=user)
                return Response({
                    'token': token.key,
                    'user_id': user.pk,
                    'username': user.username,
                    'email': user.email
                }, status=201)
        except IntegrityError:
            return Response({'error': 'O usuário já existe!'}, status=400)



class UserInfo(APIView):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    def get(self, request, format=None):
        user = User.objects.get(username=request.user)
        token, created = Token.objects.get_or_create(user=user)
        return Response({
            'token': token.key,
            'user_id': user.pk,
            'username': user.username,
            'email': user.email
        }, status=201)


class StoreList(ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Store.objects.all()
    serializer_class = StoreSerializer


class TransactionsList(ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = Transaction.objects.all()
    serializer_class = TransactionSerializer

    def get_queryset(self):
        queryset = self.queryset
        store_id = self.request.GET.get('store_id')
        if store_id:
            queryset = queryset.filter(store__id=store_id)
        return queryset

class TypeTransactionsList(ModelViewSet):
    authentication_classes = [SessionAuthentication, TokenAuthentication]
    permission_classes = [IsAuthenticated]
    queryset = TransactionType.objects.all()
    serializer_class = TransactionTypeSerializer
