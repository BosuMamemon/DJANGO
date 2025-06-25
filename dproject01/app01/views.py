import urllib.parse

from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect
from django.views.decorators.csrf import csrf_exempt
from .models import Board, Comment
from django.db.models import Q
import math

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

# def list(request):
#     board_list = Board.objects.all()
#     board_count = Board.objects.all().count
#     # print("board_list.query:", board_list.query)
#     context = {
#         'board_list': board_list,
#         'board_count': board_count
#     }
#
#     # render(리퀘스트객체, 요청주소, 담고갈dict정보)
#     return render(request, 'board/list.html', context)

# 검색포함 전체 보기
def list(request):
    word = request.GET.get('word', '')  # 기본값을 주고 싶을 때는 저렇게 두번째 값을 줌
    field = request.GET.get('field', 'title')
    page = request.GET.get('page', 1)

    if field == 'all':
        board_list = Board.objects.filter(
            Q(writer__contains=word) | Q(title__contains=word) | Q(content__contains=word)
        ).order_by('-idx')
    elif field == 'writer':
        board_list = Board.objects.filter(Q(writer__contains=word)).order_by('-idx')
    elif field == 'title':
        board_list = Board.objects.filter(Q(title__contains=word)).order_by('-idx')
    elif field == 'content':
        board_list = Board.objects.filter(Q(content__contains=word)).order_by('-idx')
    else:
        board_list = Board.objects.all().order_by('-idx')

    if field == 'all':
        board_count = Board.objects.filter(
            Q(writer__contains=word) | Q(title__contains=word) | Q(content__contains=word)
        ).count()
    elif field == 'writer':
        board_count = Board.objects.filter(Q(writer__contains=word)).count()
    elif field == 'title':
        board_count = Board.objects.filter(Q(title__contains=word)).count()
    elif field == 'content':
        board_count = Board.objects.filter(Q(content__contains=word)).count()
    else:
        board_count = Board.objects.all().count()

    block_page = 3
    page_size = 5
    current_page = int(page)
    total_page = math.ceil(board_count / page_size)
    start_page = math.floor((current_page - 1) / block_page) * block_page + 1
    end_page = start_page + block_page - 1
    if end_page > total_page:
        end_page = total_page

    context = {
        'board_list': board_list,
        'board_count': board_count,
        'start_page': start_page,
        'block_page': block_page,
        'current_page': current_page,
        'end_page': end_page,
        'total_page': total_page,
        'range': range(start_page, end_page + 1),
        'field': field,
        'word': word,
    }
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