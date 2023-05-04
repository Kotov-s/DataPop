from django.urls import path, include
from . import views

urlpatterns = [
    path('', views.chat ),
    path('chat/return_message', views.return_message ),
]