from django.db import models

# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Book(models.Model):
    title = models.CharField(max_length=200)    # 书名
    author = models.CharField(max_length=100)    # 作者
    isbn = models.CharField(max_length=13, unique=True)
    published_date = models.DateField()    # 出版时间
    quantity = models.IntegerField(default=1)    # 数量

    def __str__(self):
        return self.title

class BorrowRecord(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)    # 用户
    book = models.ForeignKey(Book, on_delete=models.CASCADE)    # 关联外键
    borrow_date = models.DateField(auto_now_add=True)    # 借出日期
    due_date = models.DateField()    # 归还日期
    returned = models.BooleanField(default=False)    # 归还状态

    def __str__(self):
        return f"{self.user.username} - {self.book.title}"