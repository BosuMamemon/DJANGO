import math
import urllib

from django.core.paginator import Paginator
from django.db.models import Q
from django.http import JsonResponse, HttpResponse
from django.shortcuts import render, redirect

from .form import UserForm
from .models import Board, Comment

UPLOAD_DIR = "C:/JHM/학습 workspace/DJANGO/upload/"


# Create your views here.
def home(request):
    return render(request, "base.html")


def insert_form(request):
    return render(request, "board/insert.html")


def insert(request):
    file_name = ""
    file_size = 0
    if "file" in request.FILES:
        file = request.FILES.get("file")
        file_name = file.name
        file_size = file.size
        fp = open("%s%s" % (UPLOAD_DIR, file_name), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

    dto = Board(
        writer=request.POST.get("writer"),
        title=request.POST.get("title"),
        content=request.POST.get("content"),
        file_name=file_name,
        file_size=file_size,
    )
    dto.save()
    return redirect("/board_list/")


def board_list(request):
    word = request.GET.get("word", "")
    field = request.GET.get("field", "title")

    if field == "all":
        board_list = Board.objects.filter(
            Q(writer__contains=word)
            | Q(title__contains=word)
            | Q(content__contains=word)
        ).order_by("-idx")
    elif field == "writer":
        board_list = Board.objects.filter(Q(writer__contains=word)).order_by("-id")
    elif field == "title":
        board_list = Board.objects.filter(Q(title__contains=word)).order_by("-id")
    elif field == "content":
        board_list = Board.objects.filter(Q(content__contains=word)).order_by("-id")
    else:
        board_list = Board.objects.all().order_by("-id")

    if field == "all":
        board_count = Board.objects.filter(
            Q(writer__contains=word)
            | Q(title__contains=word)
            | Q(content__contains=word)
        ).count()
    elif field == "writer":
        board_count = Board.objects.filter(Q(writer__contains=word)).count()
    elif field == "title":
        board_count = Board.objects.filter(Q(title__contains=word)).count()
    elif field == "content":
        board_count = Board.objects.filter(Q(content__contains=word)).count()
    else:
        board_count = Board.objects.all().count()

    page = request.GET.get("page", 1)
    block_page = 3
    page_size = 5
    current_page = int(page)
    total_page = math.ceil(board_count / page_size)
    start_page = math.floor((current_page - 1) / block_page) * block_page + 1
    end_page = start_page + block_page - 1
    if end_page > total_page:
        end_page = total_page

    context = {
        "board_list": board_list,
        "board_count": board_count,
        "start_page": start_page,
        "block_page": block_page,
        "current_page": current_page,
        "end_page": end_page,
        "total_page": total_page,
        "range": range(start_page, end_page + 1),
        "field": field,
        "word": word,
    }
    return render(request, "board/board_list.html", context)


def detail(request):
    board = Board.objects.get(id=request.GET.get("id"))
    board.hit_up()
    board.save()
    return render(request, "board/detail.html", {"dto": board})


def download_count(request):
    board = Board.objects.get(id=request.GET["id"])
    board.down_up()
    board.save()
    return JsonResponse({"count": board.down, "id": request.GET["id"]})


def download(request):
    board = Board.objects.get(id=request.GET["id"])
    path = UPLOAD_DIR + board.file_name
    file_name = urllib.parse.quote(board.file_name)

    with open(path, "rb") as file:
        response = HttpResponse(file.read(), content_type="application/octet-stream")
        response["Content-Disposition"] = "attachment;filename*=UTF-8''{0}".format(
            file_name
        )

    return response


def delete(request, id):
    board = Board.objects.get(id=id)
    board.delete()
    return redirect("/board_list/")


def update_form(request, id):
    board = Board.objects.get(id=id)
    context = {"board": board}
    return render(request, "board/update.html", context)


def update(request, id):
    board = Board.objects.get(id=id)
    file_name = board.file_name
    file_size = board.file_size
    if "file" in request.FILES:
        file = request.FILES.get("file")
        file_name = file.name
        file_size = file.size
        fp = open("%s%s" % (UPLOAD_DIR, file_name), "wb")
        for chunk in file.chunks():
            fp.write(chunk)
        fp.close()

    dto_update = Board(
        id=id,
        writer=request.POST["writer"],
        title=request.POST["title"],
        content=request.POST["content"],
        file_name=file_name,
        file_size=file_size,
    )
    dto_update.save()

    return redirect("/board_list/")


def comment_insert(request, id):
    board = Board.objects.get(id=id)
    dto = Comment(
        writer=request.POST["writer"], content=request.POST["content"], board=board
    )
    dto.save()
    return redirect("/detail/?id=" + str(id))


def board_page(request):
    page = request.GET.get("page", 1)
    word = request.GET.get("word", "")
    boards = Board.objects.filter(
        Q(writer__contains=word) | Q(title__contains=word) | Q(content__contains=word)
    )
    board_count = boards.count()
    board_list = boards.order_by("-id")

    page_size = 5
    paginator = Paginator(board_list, page_size)
    page_obj = paginator.get_page(page)

    context = {"board_count": board_count, "page_list": page_obj, "word": word}

    return render(request, "board/board_page.html", context)


def sign_up(request):
    if request.method == "POST":
        form = UserForm(request.POST)
        if form.is_valid():
            form.save()
        else:
            print(form.errors)
    else:
        form = UserForm()
    return render(request, "board/sign_up.html", {"form": form})
