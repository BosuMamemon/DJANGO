from datetime import datetime
from django.db import models


# Create your models here.
class Board(models.Model):
    writer = models.CharField(null=False, max_length=50)
    title = models.CharField(null=False, max_length=200)
    content = models.TextField(null=False)
    hit = models.IntegerField(default=0)
    post_date = models.DateField(default=datetime.now, blank=True)
    file_name = models.CharField(null=True, blank=True, default="", max_length=500)
    file_size = models.IntegerField(default=0)
    down = models.IntegerField(default=0)

    def hit_up(self):
        self.hit += 1

    def down_up(self):
        self.down += 1


class Comment(models.Model):
    board = models.ForeignKey(Board, on_delete=models.CASCADE)
    writer = models.CharField(null=False, max_length=50)
    content = models.TextField(null=False)
    post_date = models.DateField(default=datetime.now, blank=True)
