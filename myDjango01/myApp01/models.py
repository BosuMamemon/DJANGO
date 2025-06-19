from django.db import models

# Create your models here.

class Board(models.Model):
    idx = models.AutoField(primary_key=True)    # 기본 키 auto increment
    writer = models.CharField(max_length=50, null=False)
    title = models.CharField(max_length=100, null=False)
    content = models.TextField(null=False)