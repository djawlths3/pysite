import math



from django.db.models.functions import Ceil, datetime
from django.db.models import Max, F
from django.http import HttpResponseRedirect
from django.shortcuts import render



from board.boardmodule import paging
from board.models import Board


def list(request):
    pageno = int(request.GET.get('p',1))
    kwd = str(request.POST.get('kwd',''))

    pagesawcnt = 5

    boardlist = Board.objects.all().filter(title__contains=kwd).order_by('-groupno', 'orderno')[(pageno -1)*pagesawcnt : (pageno -1)*pagesawcnt +  pagesawcnt]
    total = Board.objects.filter(title__contains=kwd).count()
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
    if request.session.get('authuser') == None:
        return HttpResponseRedirect('/user/loginform')
    id = request.GET.get('id','')
    # boardlist = Board.objects.all().order_by('-id')
    data = {
        'id': id
    }
    return render(request ,'board/write.html', data)


def add(request):
    if request.session.get('authuser') == None:
        return HttpResponseRedirect('/user/loginform')

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
        board.groupno = parent.groupno
        board.orderno = parent.orderno + 1
        Board.objects.filter(groupno=board.groupno).filter(orderno__gte=board.orderno).update(orderno=F('orderno') + 1)
        board.depth = parent.depth + 1
    else:
        lastboard = Board.objects.order_by('id').last()
        if lastboard == None:
            board.groupno = 1
        else:
            board.groupno = lastboard.id +1


    board.save()

    return HttpResponseRedirect('/board')


def viewdetail(request, id):
    if request.session.get('authuser') is None:
        return HttpResponseRedirect('/user/loginform')
    boarddata = Board.objects.get(id=id)
    authuser = request.session['authuser']
    delandmodify = False

    if authuser['id'] == boarddata.user.id:
        delandmodify = True
    data = {
        'boarddata': boarddata,
        'delandmodify': delandmodify
    }
    response = render(request ,'board/view.html', data)

    tomorrow = datetime.datetime.replace(datetime.datetime.now(), hour=23, minute=59, second=0)
    expires = datetime.datetime.strftime(tomorrow, "%a, %d-%b-%Y %H:%M:%S GMT")
    cookie_id = str(authuser['id'])
    # 쿠키 값을 확인 없으면 만든다
    if cookie_id not in request.COOKIES:
        # 조회수 1 증가
        print('여기가어디라고들어오느냐')
        print(request.COOKIES)
        Board.objects.filter(id=id).update(hit=F('hit')+1)
        response.set_cookie(cookie_id, str(id), expires =expires)
    else:
        boardlist = request.COOKIES[cookie_id].split('//')
        if str(id) not in boardlist:
            Board.objects.filter(id=id).update(hit=F('hit') + 1)
            response.set_cookie(cookie_id, request.COOKIES[cookie_id]+'//'+str(id), expires=expires)

    return response

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

def delete(request):
    if request.session.get('authuser') == None:
        return HttpResponseRedirect('/user/loginform')
    no = request.GET.get('id')
    authuser = request.session['authuser']
    boarddata = Board.objects.get(id=no)

    if authuser is None:
        return HttpResponseRedirect('/board')

    if authuser['id'] != boarddata.user.id:
        return HttpResponseRedirect('/board?result=fail')

    if boarddata.delyn == 'Y':
        return HttpResponseRedirect('/board')

    Board.objects.filter(id=no).update(title='삭제된 글 입니다', content='',delyn='Y')

    return  HttpResponseRedirect('/board/')