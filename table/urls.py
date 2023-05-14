from django.contrib import admin
from django.urls import path, include
from django.contrib.auth.decorators import login_required
from . import views

urlpatterns = [
    path('', login_required(views.table)),
    path('delete/<int:pk>', login_required(views.delete_thread)),
    path('update/<int:pk>', login_required(views.update)),
    path('download/<int:pk>', login_required(views.download))
]