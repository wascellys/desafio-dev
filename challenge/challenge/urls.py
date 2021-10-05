
from django.contrib import admin
from django.urls import path, include
from rest_framework import routers

from transactions.views import stores, cadastro_page, cadastrar, login_page, register, store_details , logout_page

urlpatterns = [
    path('', login_page, name='login'),
    path('admin/', admin.site.urls),
    path('store-page/', stores, name='store-page'),
    path('insert-page/', cadastro_page, name='insert-page'),
    path('cadastrar/', cadastrar, name='cadastrar'),
    path('oauth/', include('social_django.urls', namespace='social')),
    path('login/', login_page, name='login'),
    path('logout/', logout_page, name='logout'),
    path('register/', register, name='register'),
    path('detail-page/<int:id>', store_details, name="detail-page"),
    path('api/', include('api.urls')),
]
