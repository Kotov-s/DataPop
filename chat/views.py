from django.shortcuts import render
from django.templatetags.static import static
from django.http import JsonResponse, HttpResponseRedirect, Http404
from .forms import FileForm
import os
from django.conf import settings
from django.utils import timezone
from .models import Threads, Message
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied

def chat(request, user_id, csv_slug):
    if user_id != request.user.id:
        raise PermissionDenied
    if not Threads.objects.filter(user=request.user, slug=csv_slug).exists():
        raise Http404
    
    thread = Threads.objects.get(user=request.user, slug=csv_slug)
    messages = Message.objects.filter(thread=thread)
    context = {
        'bot_avatar': static('chat/img/bot_avatar.jpg'),
        'user_avatar': static('chat/img/user_avatar.jpg'),
        'user_id': user_id,
        'csv_slug': csv_slug,
        'messages': messages
    }
    return render(request, 'chat/chat.html', context)

def file_form(request):
    if request.method == "POST":
        # create a form instance and populate it with data from the request:
        form = FileForm(request.POST, request.FILES)
        # check whether it's valid:
        if form.is_valid():
            # process the data in form.cleaned_data as required
            file = request.FILES['file']
            file_name = 'data.csv'
            user_folder = f'users/user_{request.user.id}/csv'
            user_folder_path = os.path.join(settings.MEDIA_ROOT, user_folder)
            os.makedirs(user_folder_path, exist_ok=True)
            file_path = os.path.join(user_folder_path, file_name)
            # Check if a file with the same name already exists and rename the uploaded file if necessary
            unique_file_path = file_path
            i = 1
            while os.path.exists(unique_file_path):
                name, ext = os.path.splitext(file_name)
                unique_file_path = os.path.join(user_folder_path, f'{name}_{i}{ext}')
                i += 1
            with open(unique_file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # inserting data into database
            formatted_time = timezone.now().strftime('%Y-%m-%d %H:%M:%S')\

            thread = Threads.objects.create(
                user=User.objects.get(id=request.user.id),
                csv_path=unique_file_path,
                slug=f'{file_name[:-4]}_{i-1}',
                title=f'The post was created in {formatted_time}'
            )
            generate_report(thread.id, thread.slug, thread.user_id)
            return HttpResponseRedirect(f"/chat/{request.user.id}/{file_name[:-4]}_{i-1}")

    # if a GET (or any other method) we'll create a blank form
    else:
        context = {
            'form' : FileForm(),
        }
        
    return render(request, "chat/form.html", context)

def generate_report(thread_id, csv_name, user_id):
    user_folder = f'users/user_{user_id}/media/{csv_name}'
    user_folder_path = os.path.join(settings.MEDIA_ROOT, user_folder)
    os.makedirs(user_folder_path, exist_ok=True)

    file_path = os.path.join(user_folder_path, 'first.html')

    with open(file_path, 'w') as f:
        f.write('<h1>HI!</h1>')

    Message.objects.create(
        thread=Threads.objects.get(id=thread_id),
        title='Here is first report',
        content_path=file_path
    )



def return_message(request, user_id, csv_slug):
    return render(request, 'explanations/first.html')
    # keyWord = request.GET.get('result', None)
    # HEADERS = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:84.0) Gecko/20100101 Firefox/84.0',
    #            'accept': '*/*'}
    # URL = 'https://www.anekdot.ru/search/?query='
    # url = f'{URL}{keyWord}'
    # try:
    #     response = requests.get(url, headers=HEADERS)
    # except requests.ConnectionError:
    #     return JsonResponse({'result': 'Сетевая ошибка'})
    # if response.status_code == 200:
    #     soup = BeautifulSoup(response.text, 'html.parser')
    #     try:
    #         jokes = soup.find_all(
    #             'div', {'class': 'topicbox'})
    #         joke = str(jokes[0].find(
    #             'div', {'class': 'text'})).replace('<span style="background-color:#ffff80">', '')
    #         return JsonResponse({'result': joke})
    #     except:
    #         return JsonResponse({'result': 'По вашему запросу ничего не найдено.'})
    # else:
    #     return JsonResponse({'result': 'Ошибка на сервере'})