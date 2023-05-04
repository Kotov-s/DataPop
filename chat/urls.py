from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('chat', login_required(views.chat) ),
    path('', login_required(views.file_form) ),
    path('chat/return_message', login_required(views.return_message) ),
]