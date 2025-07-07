import os
import uuid

from django.contrib.auth.hashers import make_password, check_password
from django.core.paginator import Paginator
from django.db.models import Q
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from PyCharmTest import settings
from .forms import PostCreateForm, PostUpdateForm
from .imagePro import data_pro, data_pro2
from .models import Post


# Create your views here.
# 게시글 등록
def create_post(request):
    form = PostCreateForm()
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.password = make_password(form.cleaned_data["password"])
            # 파일 업로드
            file = request.FILES.get("upload_file")
            if file:
                filename = uuid.uuid4().hex
                # 파일 저장 경로
                file_path = os.path.join(settings.MEDIA_ROOT, 'test_app', str(post.id), str(filename))
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path))
                # 파일 저장
                save_path = file_path + file.name
                with open(save_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                post.filename = filename
                post.original_filename = file.name
            post.save()
            messages.success(request, "게시글이 등록되었습니다.")
            return redirect("test_app:read", post_id=post.id)
        else:
            messages.error(request, "게시글 등록에 실패했습니다.")
    return render(request,"posts/create.html", {"form": form})


# 게시글 보기
def get_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    return render(request, "posts/read.html", {"post": post})

def update_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        # 비밀번호 확인
        if not check_password(request.POST.get("password"), post.password):
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            form = PostUpdateForm(instance=post)
            return render(request, "posts/update.html", {"form": form})
            
        # 비밀번호가 일치하면 폼 처리
        form = PostUpdateForm(request.POST, instance=post)
        if form.is_valid():
            post = form.save(commit=False)
            post.password = make_password(form.cleaned_data["password"])  # 새 비밀번호 해시화
            
            # 파일 삭제
            if form.cleaned_data["delete_file"]:
                if post.filename:
                    file_path = os.path.join(settings.MEDIA_ROOT, "test_app", str(post.id), str(post.filename))
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    post.filename = None
                    post.original_filename = None
                    
            # 파일 업로드
            file = request.FILES.get("upload_file")
            if file:
                if post.filename:
                    file_path = os.path.join(settings.MEDIA_ROOT, "test_app", str(post.id), str(post.filename))
                    if os.path.exists(file_path):
                        os.remove(file_path)
                    post.filename = None
                    post.original_filename = None
                filename = uuid.uuid4().hex
                file_path = os.path.join(settings.MEDIA_ROOT, "test_app", str(post.id), str(filename))
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path))
                with open(file_path, "wb") as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                post.filename = filename
                post.original_filename = file.name
                
            post.save()
            messages.success(request, "게시글이 수정되었습니다.")
            return redirect("test_app:read", post_id=post.id)
        else:
            messages.error(request, "게시글 수정에 실패했습니다.")
    else:
        form = PostUpdateForm(instance=post)
        
    return render(request, "posts/update.html", {"form": form})

# 게시글 삭제
def delete_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    if request.method == "POST":
        if check_password(request.POST.get("password"), post.password):
            if post.filename:
                file_path = os.path.join(settings.MEDIA_ROOT, "test_app", str(post.id), str(post.filename))
                if os.path.exists(file_path):
                    os.remove(file_path)
            post.delete()
            messages.success(request, "게시글이 삭제되었습니다.")
            return redirect("test_app:list")
        else:
            messages.error(request, "비밀번호가 일치하지 않습니다.")
            return redirect("test_app:read", post_id=post.id)

    return HttpResponse('게시글 삭제')

# 게시글 목록
def get_posts(request):
    page = request.GET.get('page', '1')
    searchType = request.GET.get('searchType')
    searchKeyword = request.GET.get('searchKeyword')
    posts = Post.objects.all().order_by('-created_at')

    # 검색 조건 처리
    if searchType not in [None, ''] and searchKeyword not in [None, '']:
        if searchType == 'all':
            posts = posts.filter(
                Q(title__contains=searchKeyword) |
                Q(content__contains=searchKeyword) |
                Q(username__contains=searchKeyword)
            )
        elif searchType == 'title':
            posts = posts.filter(
                Q(title__contains=searchKeyword)
            )
        elif searchType == 'content':
            posts = posts.filter(
                Q(content__contains=searchKeyword)
            )
        elif searchType == 'username':
            posts = posts.filter(
                Q(username__contains=searchKeyword)
            )

    # 페이지네이션
    paginator = Paginator(posts, 10)
    page_obj = paginator.get_page(page)

    # 현재 페이지의 첫 번째 게시글 번호 계산
    start_index = paginator.count - (paginator.per_page * (page_obj.number - 1))

    # 순번 계산하여 게시글 리스트에 추가
    for index, _ in enumerate(page_obj, start=0):
        page_obj[index].index_number = start_index - index

    return render(request, 'posts/list.html', {
        'posts': page_obj,
        'searchType': searchType,
        'searchKeyword': searchKeyword,
    })

def download_file(request):
    return

def image_test(request):
    predict = data_pro()
    return render(
        request,
        "imagePro/image_test.html",
        {"predict": predict, "MEDIA_URL": settings.MEDIA_URL}
    )

def create_post2(request):
    form = PostCreateForm()
    if request.method == "POST":
        form = PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.password = make_password(form.cleaned_data["password"])
            # 파일 업로드
            file = request.FILES.get("upload_file")
            if file:
                filename = uuid.uuid4().hex
                # 파일 저장 경로
                file_path = os.path.join(settings.MEDIA_ROOT, 'test_app', str(post.id), str(filename))
                if not os.path.exists(os.path.dirname(file_path)):
                    os.makedirs(os.path.dirname(file_path))
                # 파일 저장
                save_path = file_path + file.name
                with open(save_path, 'wb') as f:
                    for chunk in file.chunks():
                        f.write(chunk)
                post.filename = filename
                post.original_filename = file.name
            post.save()
            messages.success(request, "게시글이 등록되었습니다.")
            predict = data_pro2(filename, post.id, file.name)
            return render(
                request,
                "imagePro/image_test2.html",
                {
                    "predict": predict,
                    "save_path": "test_app/" + str(post.id) + "/" + str(filename) + file.name,
                    "MEDIA_URL": settings.MEDIA_URL
                }
            )
        else:
            messages.error(request, "게시글 등록에 실패했습니다.")
    return render(request, "posts/create.html", {"form": form})