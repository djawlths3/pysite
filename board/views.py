import math
from builtins import int, type

from django.db.models import F
from django.db.models.functions import Ceil
from django.http import HttpResponseRedirect
from django.shortcuts import render

# Create your views here.
from board.boardmodule import paging
from board.models import Board


def list(request):
    pageno = int(request.GET.get('p',1))
    pagesawcnt = 5

    boardlist = Board.objects.all().filter(title__contains='').order_by('-id')[(pageno -1)*pagesawcnt : (pageno -1)*pagesawcnt +  pagesawcnt]
    total = Board.objects.filter(title__contains='').count()
    pagesize = math.ceil(total/pagesawcnt)
    pagelist = paging(pageno,pagesize)
    data = {
        'boardlist': boardlist,
        'pagelist': pagelist,
        'nowpage' : pageno,
        'pagesize' : pagesize
    }
    return render(request ,'board/list.html', data)


def write(request):
    id = request.GET.get('id','')
    # boardlist = Board.objects.all().order_by('-id')
    data = {
        'id': id
    }
    return render(request ,'board/write.html', data)


def add(request):
    authuser = request.session['authuser']
    paraentno = request.POST.get('parentno')

    if authuser is None:
        return HttpResponseRedirect('/board')

    board = Board()
    board.user_id = authuser['id']
    board.title = request.POST.get('title')
    board.content = request.POST.get('contents')

    if paraentno != '':
        parent = Board.objects.get(id=paraentno)
        board.groupno = paraentno.groupno
        board.orderno = parent.orderno + 1
        Board.objects.filter(groupno=board.groupno).filter(orderno__gte=board.orderno).update(orderno=F('orderno') + 1)
        board.depth = parent.depth + 1
    else:
       groupno = Board.objects.latest('id')
       board.groupno = groupno + 1

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