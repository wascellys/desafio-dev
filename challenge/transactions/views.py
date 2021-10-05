import os

import requests
from django.contrib import messages
from django.contrib.auth import logout, authenticate, login
from django.contrib.auth.decorators import login_required
from django.core.exceptions import ObjectDoesNotExist
from django.db import transaction
from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import render, redirect
from api.models import Store
from rest_framework.authtoken.models import Token

URL = "http://localhost:8000/api"


def login_page(request):
    if request.method == 'POST':
        data = {}
        data['username'] = request.POST.get('username')
        data['password'] = request.POST.get('password')
        r = requests.post(URL+'/api-token-auth/', data=data)

        if r.status_code == 200:
            user = authenticate(username=data['username'], password=data['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return redirect('store-page')
        else:
            messages.error(request, "Dados de acesso incorretos!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    else:
        if request.user.is_authenticated:
            return redirect('store-page')

    return render(request, 'auth/login.html')

def register(request):
    if request.method == 'POST':

        data = {}
        data['username'] = request.POST.get('username')
        data['email'] = request.POST.get('username')
        data['password'] = request.POST.get('password')
        r = requests.post(URL + '/register/', data=data)

        if r.status_code == 201:
            return login_page(request)
        else:
            messages.error(request, "Erro ao tentar criar o cadastro. Tente novamente!")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


    return render(request, 'auth/register.html')



def logout_page(request):
    logout(request)
    return render(request, 'auth/login.html')

@login_required
def stores(request):
    return render(request, 'financial/store-page.html')

@login_required
def cadastro_page(request):
    return render(request, 'financial/insert-transaction-page.html')

@login_required
def cadastrar(request):
    try:
        arquivo = request.FILES['file']
        files = {'file': arquivo}
        r = requests.post(URL + '/upload/file', files=files)
        if r.status_code == 201:
            messages.success(request, "Arquivo importado com sucesso! ")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

        else:
            messages.error(request, "Os dados arquivo não está no padrão esperado")
            return HttpResponseRedirect(request.META.get('HTTP_REFERER'))
    except:
        messages.error(request, "Erro ao enviar o arquivo! ")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))

@login_required
def store_details(request, id):
    try:
        store = Store.objects.get(pk=id)
        return render(request, 'financial/store-detail-page.html', {'loja': store})

    except ObjectDoesNotExist:
        messages.error(request, "A loja não existe!")
        return HttpResponseRedirect(request.META.get('HTTP_REFERER'))


