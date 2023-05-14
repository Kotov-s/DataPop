from django.shortcuts import render
from chat.models import Threads
from django.http import HttpResponseRedirect
from .forms import FileForm
from django.http import FileResponse
from django.utils.text import slugify
from unidecode import unidecode

def delete_thread(request, pk):
    thread = Threads.objects.get(id=pk)
    thread.delete()
    return HttpResponseRedirect("/table/")

def download(request, pk):
    thread = Threads.objects.get(id=pk)
    file_path = thread.edited_csv_path
    file_name = slugify(unidecode(thread.title)) + '.csv'
    response = FileResponse(open(file_path, 'rb'), content_type='application/force-download')
    response['Content-Disposition'] = 'attachment; filename="%s"' % file_name
    return response

def update(request, pk):
    thread = Threads.objects.get(id=pk)
    user_title = thread.title
    user_enable = thread.expl_enable
    form = FileForm(request.POST or None, initial={'text': user_title, 'check': user_enable})
    if request.method == "POST":
        if form.is_valid():
            title = form.cleaned_data['text']
            enabled = form.cleaned_data['check']
            thread.title = title
            thread.expl_enable = enabled
            thread.save()
            return HttpResponseRedirect(f"../")
    context = {
        'form_title': 'Обновите тред',
        'form': form,
        'title': user_title,
        'enable': user_enable
    }
    return render(request, 'form.html', context)

def table(request):
    user_id = request.user.id
    threads = Threads.objects.filter(user=user_id).order_by('-created_at')
    context = {
        'user_id': user_id,
        'threads': threads
    }
   
    return render(request, 'table/table.html', context)
