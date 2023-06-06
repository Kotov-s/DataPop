from django.shortcuts import render
from django.templatetags.static import static
from django.http import JsonResponse, HttpResponseRedirect, Http404
from .forms import FileForm
import os
from django.conf import settings
from django.utils import timezone
from .models import Threads, Message, Explanation
from django.contrib.auth.models import User
from django.core.exceptions import PermissionDenied
from . import data_analysis
import shutil
from django.template.loader import render_to_string
import uuid

def create_message(thread, my_title, file_path, explanation, message_uuid):
    expl = Explanation.objects.get(id=explanation)
    Message.objects.create(
        thread=thread,
        title=my_title,
        content_path=file_path,
        explanation = expl,
        uuid = message_uuid
    )
    thread.expl_enable
    html = render_to_string(file_path, {'title': my_title})
    data = {
        'title': my_title, 
        'html': html, 
        'explanation': expl.explanation,
        'enable': thread.expl_enable
        }
    return data


def chat(request, user_id, csv_slug):
    if user_id != request.user.id:
        raise PermissionDenied
    if not Threads.objects.filter(user=request.user, slug=csv_slug).exists():
        raise Http404
    
    thread = Threads.objects.get(user=request.user, slug=csv_slug)
    messages = Message.objects.filter(thread=thread)

    edited_csv_path = thread.edited_csv_path
    columns = data_analysis.get_columns(edited_csv_path)

    context = {
        'bot_avatar': static('chat/img/bot_avatar.jpg'),
        'user_avatar': static('chat/img/user_avatar.jpg'),
        'user_id': user_id,
        'csv_slug': csv_slug,
        'messages': messages,
        'columns': columns
    }
    return render(request, 'chat/chat.html', context)

def file_form(request):
    form = FileForm(request.POST or None, request.FILES or None)
    if request.method == "POST":
        if form.is_valid():
            file = request.FILES['file']
            title = form.cleaned_data['text']
            enabled = form.cleaned_data['check']
            
            file_name = 'data.csv'
            user_folder = f'users/user_{request.user.id}/csv'
            user_folder_path = os.path.join(settings.MEDIA_ROOT, user_folder)
            os.makedirs(user_folder_path, exist_ok=True)
            file_path = os.path.join(user_folder_path, file_name)
            # Проверка, если файл существует, иначе создаем другой номер у файла
            unique_file_path = file_path
            i = 1
            while os.path.exists(unique_file_path):
                name, ext = os.path.splitext(file_name)
                unique_file_path = os.path.join(user_folder_path, f'{name}_{i}{ext}')
                i += 1
            with open(unique_file_path, 'wb+') as destination:
                for chunk in file.chunks():
                    destination.write(chunk)

            # Копия CSV
            edited_file_name = f'edited_{file_name[:-4]}_{i-1}.csv'
            edited_file_path = os.path.join(user_folder_path, edited_file_name)
            shutil.copy2(unique_file_path, edited_file_path)

            thread = Threads.objects.create(
                user=User.objects.get(id=request.user.id),
                csv_path=unique_file_path,
                edited_csv_path=edited_file_path,
                slug=f'{file_name[:-4]}_{i-1}',
                title=title,
                expl_enable=enabled
            )
            generate_report(thread.id, thread.slug, thread.user_id, thread.csv_path)
            return HttpResponseRedirect(f"/chat/{request.user.id}/{file_name[:-4]}_{i-1}")
    return render(request, "form.html", context={'form': form, 'form_title': 'Загрузите CSV файл и начните исследовать'})

def generate_report(thread_id, csv_name, user_id, csv_path):
    user_folder = f'users/user_{user_id}/media/{csv_name}'
    user_folder_path = os.path.join(settings.MEDIA_ROOT, user_folder)
    os.makedirs(user_folder_path, exist_ok=True)

    file_path = os.path.join(user_folder_path, 'first.html')

    data_analysis.first_analysis_file(csv_path, file_path)

    expl = Explanation.objects.get(id=1)
    Message.objects.create(
        explanation = expl,
        thread=Threads.objects.get(id=thread_id),
        title='Это ваш предварительный анализ данных',
        content_path=file_path
    )


def columns_func(request, analysis_func):
    if request.method == 'POST':
        formatted_time = timezone.now().strftime('%Y_%m_%d_%H_%M_%S')

        thread_id = request.POST.get('threadId') 
        thread = Threads.objects.get(id=thread_id)
        edited_csv_path = thread.edited_csv_path 
        user_id = thread.user_id
        csv_slug = thread.slug

        # Задаем дефолтные значения
        message_uuid = uuid.uuid4()

        my_title = 'Не удалось выполнить действие'
        explanation = 1

        # Путь внутри папки chat/static/
        user_folder = f'users/user_{user_id}/{csv_slug}/img/{message_uuid}'

        if analysis_func != 'columns':
            file_path = create_file(user_id, csv_slug, analysis_func, formatted_time)

        column_name = request.POST.getlist('columnName[]')

        try:
            match analysis_func:
                case 'delete_column':
                    data_analysis.delete_column(edited_csv_path, file_path, column_name)
                    my_title = 'Удалеие столбца'

                case 'pie_plot':
                    column_name = column_name[0]
                    data_analysis.pie_plot(edited_csv_path, file_path, column_name, user_folder)
                    my_title = 'Круговая диаграмма'
                    explanation = 2

                case 'columns':
                    columns = data_analysis.get_columns(edited_csv_path)
                    data = {'columns': columns}
                    return JsonResponse(data)  

                case 'drop_na':
                    data_analysis.drop_na(edited_csv_path, file_path)
                    my_title = 'Удалеие строк с NaN'
                    explanation = 3

                case 'object_statistics':
                    data_analysis.object_statistics(edited_csv_path, file_path)
                    my_title = 'Статистика объектов'
                    explanation = 4  

                case 'all_rows':
                    data_analysis.all_rows(edited_csv_path, file_path)
                    my_title = 'Все строки'  

                case 'heatmap':
                    data_analysis.heat_map(edited_csv_path, file_path)
                    my_title='Тепловая карта' 
                    explanation = 5  

                case 'boxplot_graph':
                    data_analysis.boxplot_graph(edited_csv_path, file_path, user_folder)
                    my_title='Ящик с усами' 
                    explanation = 6

                case 'back_to_roots':
                    csv_path = thread.csv_path
                    data_analysis.back_to_roots(edited_csv_path, csv_path, file_path)
                    my_title='Исходное положение' 

                case 'non_object_statistics':
                    data_analysis.non_object_statistics(edited_csv_path, file_path)
                    my_title='Статистика не объектов' 
                    explanation = 7  

                case 'state_map_plot':
                    data_analysis.state_map_plot(edited_csv_path, file_path, column_name, user_folder)
                    my_title='Фоновая картограмма США' 
                    explanation = 8  

                case 'show_nans':
                    data_analysis.show_nans(edited_csv_path, file_path)
                    my_title='Пропущенные значения' 

                case 'bar_plot':
                    data_analysis.bar_plot(edited_csv_path, file_path, column_name, user_folder)
                    my_title='Столбцовая диаграмма' 
                    explanation = 9  

                case 'histogram_graph':
                    data_analysis.histogram_graph(edited_csv_path, file_path, user_folder)
                    my_title='Гистограммы' 
                    explanation = 10  

                case 'scatter_plot':
                    data_analysis.scatter_plot(edited_csv_path, file_path, column_name, user_folder)
                    my_title='Диаграмма рассеяния' 
                    explanation = 11  

                case 'group_by_sum':
                    data_analysis.group_by_sum(edited_csv_path, file_path, column_name)
                    my_title='Группировка (Сумма)' 
                    explanation = 11  

                case 'group_by_mean':
                    data_analysis.group_by_mean(edited_csv_path, file_path, column_name)
                    my_title='Группировка (Средние)' 
                    explanation = 11  

                case 'dendrogram':
                    data_analysis.dendrogram_plot(edited_csv_path, file_path, column_name, user_folder)
                    my_title='dendrogram' 
                    explanation = 11 

                case _:
                    my_title='Не удалось найти функцию' 
        
            data = create_message(thread, my_title, file_path, explanation, message_uuid)                 
            return JsonResponse(data) 
        except Exception:
            print(Exception)


def delete_messsage(request, pk):
    if request.method == 'POST':
        message = Message.objects.get(id=pk)
        thread = message.thread
        slug = thread.slug
        user_id = thread.user_id
        content_path = message.content_path
        
        image_folder = f'users/user_{user_id}/{thread.slug}/img/{message.uuid}'
        img_folder_path = os.path.join(settings.BASE_DIR / "chat/static/chat", image_folder)

        print(img_folder_path)


        if os.path.exists(img_folder_path):
            shutil.rmtree(img_folder_path)

        os.remove(content_path)

        message.delete()
        return HttpResponseRedirect(f"/chat/{user_id}/{slug}")

def create_file(user_id, csv_slug, file_name, formatted_time):
    # Создаем директорию
    user_folder = f'users/user_{user_id}/media/{csv_slug}'
    user_folder_path = os.path.join(settings.MEDIA_ROOT, user_folder)
    os.makedirs(user_folder_path, exist_ok=True)

    # Создаем файл для помещения в него таблицы
    file_path = os.path.join(user_folder_path, f'{file_name}{formatted_time}.html')
    return file_path