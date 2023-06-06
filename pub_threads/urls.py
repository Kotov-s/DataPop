from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', views.show ),    
    path('<int:pk>', views.show_thread ),
]