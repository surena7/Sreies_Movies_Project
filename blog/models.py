from django.db import models
from django.contrib.auth.models import User




class Post(models.Model):
    title = models.CharField(max_length=201 , verbose_name="عنوان")
    image = models.ImageField(upload_to="blog/" , verbose_name="عکس")
    text = models.TextField(verbose_name="متن")
    author = models.ForeignKey(User , on_delete=models.CASCADE , verbose_name="نویسنده")
    created = models.DateTimeField(auto_now_add=True , verbose_name="زمان ثبت")
    views = models.PositiveIntegerField(default=0 , verbose_name="بازدید ها")
    def __str__(self):
        return self.title