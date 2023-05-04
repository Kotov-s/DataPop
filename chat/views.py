from django.shortcuts import render
from django.templatetags.static import static
from bs4 import BeautifulSoup
from django.http import JsonResponse, HttpResponse
import requests
# Create your views here.

def chat(request):
    context = {
        'bot_avatar': static('chat/img/bot_avatar.jpg'),
        'user_avatar': static('chat/img/user_avatar.jpg'),
    }
    return render(request, 'chat/chat.html', context)


def return_message(request):
    keyWord = request.GET.get('result', None)
    print(keyWord)
    HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
               'accept': '*/*'}
    URL = 'https://www.anekdot.ru/search/?query='
    url = f'{URL}{keyWord}'
    try:
        response = requests.get(url, headers=HEADERS)
    except requests.ConnectionError:
        return JsonResponse({'result': 'Сетевая ошибка'})
    if response.status_code == 200:
        soup = BeautifulSoup(response.text, 'html.parser')
        try:
            jokes = soup.find_all(
                'div', {'class': 'topicbox'})
            joke = str(jokes[0].find(
                'div', {'class': 'text'})).replace('<span style="background-color:#ffff80">', '')
            return JsonResponse({'result': joke})
        except:
            return JsonResponse({'result': 'По вашему запросу ничего не найдено.'})
    else:
        return JsonResponse({'result': 'Ошибка на сервере'})