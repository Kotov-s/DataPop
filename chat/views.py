from django.shortcuts import render
from django.templatetags.static import static
# Create your views here.

def chat(request):
    context = {
        'bot_avatar': static('chat/img/bot_avatar.jpg'),
        'user_avatar': static('chat/img/user_avatar.jpg'),
    }
    return render(request, 'chat/html/chat.html', context)