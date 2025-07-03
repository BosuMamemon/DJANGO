from django.shortcuts import render
from django.views.decorators.csrf import csrf_exempt
from myApp01.models import Board

# Create your views here.


# 추가 폼으로 이동
def write_form(request):
    return render(request, "board/write.html")


# 추가
@csrf_exempt
def insert(request):
    dto = Board(
        writer=request.POST["writer"],
        title=request.POST["title"],
        content=request.POST["content"],
    )
    dto.save()
    return render(request, "board/write.html")
