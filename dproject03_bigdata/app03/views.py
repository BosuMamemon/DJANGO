from django.shortcuts import render
from . import bigdata_process


# Create your views here.
def home(request):
    return render(request, "base.html")


def melon(request):
    datas = bigdata_process.melon_crawling()
    return render(request, "bigdata/melon.html", {"datas": datas})


def movie(request):
    datas = bigdata_process.movie_crawling()
    return render(request, "bigdata/movie.html", {"datas": datas})


def movie_chart(request):
    image_dic = bigdata_process.movie_chart_crawling()
    return render(request, "bigdata/movie_chart.html", {"datas": image_dic})


def starbucks(request):
    datas = bigdata_process.starbucks()
    return render(request, "bigdata/starbucks.html", {"datas": datas})
