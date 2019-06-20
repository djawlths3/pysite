from django.http import HttpResponseRedirect
from django.shortcuts import render
from guestbook.models import Guestbook

# Create your views here.


def list(request):
    guestbooklist = Guestbook.objects.all().order_by('-id')
    data = {
        'guestbooklist': guestbooklist
    }
    return render(request ,'guestbook/list.html', data)

def add(request):
    guestbook = Guestbook()
    guestbook.name = request.POST['name']
    guestbook.contents = request.POST['contents']
    guestbook.password = request.POST['password']

    guestbook.save()
    return HttpResponseRedirect('/guestbook')

def deleteform(request, id):
    data = {
        'no': id
    }
    return render(request, 'guestbook/deleteform.html', data)

def delete(request):
    guestbook = Guestbook()
    guestbook.id = request.POST['no']
    guestbook.password = request.POST['password']
    guestbook = Guestbook.objects.filter(id=guestbook.id).filter(password=guestbook.password)
    guestbook.delete()
    return HttpResponseRedirect('/guestbook')