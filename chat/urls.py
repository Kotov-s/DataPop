from django.urls import path, include
from django.contrib.auth.decorators import login_required

from . import views

urlpatterns = [
    path('', login_required(views.file_form) ),

    path('chat/<int:user_id>/<slug:csv_slug>', login_required(views.chat) ),
    path('chat/delete/message/<int:pk>', login_required(views.delete_messsage) ),

    # data analysis     
    path('chat/<slug:analysis_func>', login_required(views.columns_func) ),
]