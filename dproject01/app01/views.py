import urllib.parse

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from app01.models import Board, Comment

# Create your views here.
UPLOAD_DIR = "C:/JHM/학습 workspace/DJANGO/upload/"

def write_form(request):
    return render(request, "board/write_form.html")

@csrf_exempt
def write(request):
    fname = ''
    fsize = 0
    if 'file' in request.FILES:
        file = request.FILES['file']
        fsize = file.size
        fname = file.name
        fp = open('%s%s' %(UPLOAD_DIR, fname), 'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

    dto = Board(
        writer=request.POST['writer'],
        title=request.POST['title'],
        content=request.POST['content'],
        file_name=fname,
        file_size=fsize
    )
    dto.save()

    return redirect("/list/")

def list(request):
    board_list = Board.objects.all()
    board_count = Board.objects.all().count
    # print("board_list.query:", board_list.query)
    context = {
        'board_list': board_list,
        'board_count': board_count
    }

    # render(리퀘스트객체, 요청주소, 담고갈dict정보)
    return render(request, 'board/list.html', context)

def detail_idx(request):
    idx = request.GET['idx']
    dto = Board.objects.get(idx=idx)
    comment_list = Comment.objects.filter(board_idx=idx).order_by('-idx')
    comment_count = Comment.objects.filter(board_idx=idx).count
    print("comment_list.query:", comment_list.query)
    context = {
        "dto": dto,
        'comment_list': comment_list,
        'comment_count': comment_count
    }
    dto.hit_up()
    dto.save()
    return render(request, 'board/detail.html', context)

def detail(request, board_idx):
    dto = Board.objects.get(idx=board_idx)
    comment_list = Comment.objects.filter(board_idx=board_idx).order_by('-board_idx')
    comment_count = Comment.objects.filter(board_idx=board_idx).count
    print("comment_list.query:", comment_list.query)
    context = {
        "dto": dto,
        'comment_list': comment_list,
        'comment_count': comment_count
    }
    dto.hit_up()
    dto.save()
    return render(request, 'board/detail.html', context)

def delete(request, board_idx):
    Board.objects.get(idx=board_idx).delete()
    return redirect("/list/")

def update_form(request, board_idx):
    dto = Board.objects.get(idx=board_idx)
    dto.hit_up()
    dto.save()
    context = {'dto': dto}
    return render(request, "board/update_form.html", context)

@csrf_exempt
def update(request):
    dto = Board.objects.get(idx=request.POST['idx'])

    fname = dto.file_name
    fsize = dto.file_size
    if 'file' in request.FILES:
        file = request.FILES['file']
        fsize = file.size
        fname = file.name
        fp = open('%s%s' %(UPLOAD_DIR, fname), 'wb')
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

    dto_update = Board(
        idx=request.POST['idx'],
        writer=request.POST['writer'],
        title=request.POST['title'],
        content=request.POST['content'],
        file_name=fname,
        file_size=fsize
    )
    dto_update.save()
    return redirect("/list/")

def download_count(request):
    idx = request.GET['idx']
    dto = Board.objects.get(idx=idx)
    dto.down_up()
    dto.save()
    count = dto.down
    print("count", count)

    return JsonResponse({'count': count, 'idx': idx})

def download(request):
    idx = request.GET['idx']
    dto = Board.objects.get(idx=idx)
    path = UPLOAD_DIR + dto.file_name
    file_name = urllib.parse.quote(dto.file_name)

    with open(path, 'rb') as file:
        response = HttpResponse(file.read(), content_type='application/octet-stream')
        response['Content-Disposition'] = "attachment;filename*=UTF-8''{0}".format(file_name)

    return response

@csrf_exempt
def comment_insert(request):
    dto = Comment(
        board_idx=request.POST['idx'],
        writer=request.POST['writer'],
        content=request.POST['content'],
    )
    dto.save()
    return redirect("/detail/" + request.POST['idx'])