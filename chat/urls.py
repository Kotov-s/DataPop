from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('chat/<int:user_id>/<slug:csv_slug>', login_required(views.chat) ),
    path('', login_required(views.file_form) ),

    # ajax requests      
    path('chat/<slug:analysis_func>', login_required(views.columns_func) ),
]