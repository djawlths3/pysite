from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.models import Board


def list(request):
    boardlist = Board.objects.all().order_by('-id')
    data = {
        'boardlist': boardlist
    }
    return render(request ,'board/list.html', data)


def write(request):
    boardlist = Board.objects.all().order_by('-id')
    data = {
        'guestbooklist': boardlist
    }
    return render(request ,'board/write.html', data)


def add(request):
    authuser = request.session['authuser']

    if authuser is None:
        return HttpResponseRedirect('/board')

    board = Board()
    board.user_id = authuser['id']
    board.title = request.POST.get('title')
    board.content = request.POST.get('contents')
    board.save()

    return HttpResponseRedirect('/board')

def viewdetail(request, id):
    boarddata = Board.objects.get(id=id)
    authuser = request.session['authuser']
    delandmodify = False
    if authuser['id'] == boarddata.user.id:
        delandmodify = True
    data = {
        'boarddata': boarddata,
        'delandmodify' :  delandmodify
    }

    return render(request ,'board/view.html', data)

def modify(request):
    no = request.GET.get('id')
    authuser = request.session['authuser']
    boarddata = Board.objects.get(id=no)

    if authuser is None:
        return HttpResponseRedirect('/board')

    if authuser['id'] != boarddata.user.id:
        return HttpResponseRedirect('/board')

    data = {
        'boarddata': boarddata
    }

    return render(request ,'board/modify.html', data)

def modifypost(request):
    no = request.GET.get('id')
    authuser = request.session['authuser']
    boarddata = Board.objects.get(id=no)

    if authuser is None:
        return HttpResponseRedirect('/board')

    if authuser['id'] != boarddata.user.id:
        return HttpResponseRedirect('/board')
    Board.objects.filter(id=no).update(title=request.POST.get('title'), content=request.POST.get('contents'))

    return  HttpResponseRedirect('/board/view/{0}'.format(no))