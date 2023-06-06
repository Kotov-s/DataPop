from django.shortcuts import render
from chat.models import Threads, Message
from django.http import HttpResponseForbidden
from django.core.paginator import Paginator


def show(request):
    search_string = request.GET.get('search', '')
    if not search_string:
        threads = Threads.objects.filter(is_public=True)
    else:
        threads = Threads.objects.filter(is_public=True, title__icontains=search_string)

    paginator = Paginator(threads, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    context = {
        'page_obj': page_obj,
        'paginator': paginator,
        'search_string': search_string
    }
    return render(request, 'pub_threads/threads.html', context)

        

def show_thread(request, pk):
    thread = Threads.objects.get(id=pk)

    if thread.is_public:
        messages = Message.objects.filter(thread=thread)
        context = {
            'thread' : thread,
            'messages': messages
            } 
        
        return render(request, 'pub_threads/thread.html', context)
    else:
        return HttpResponseForbidden()
