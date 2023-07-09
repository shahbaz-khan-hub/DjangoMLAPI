
from django.contrib import admin
from django.urls import path 
from django.urls import include

urlpatterns = [
    path('admin/', admin.site.urls, name='admin'),
    path('',include('carmodel.urls')),
]
 