from django.db import models
from django.contrib.auth.models import User
from web.models import Movies




class Comment(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , verbose_name="کاربر")
    movie = models.ForeignKey(Movies , on_delete=models.CASCADE , verbose_name="فیلم")
    text = models.TextField(verbose_name="متن")
    created = models.DateTimeField(auto_now_add=True , verbose_name="زمان ثبت")
    def __str__(self):
        return f"{self.user.username}_{self.text[0:50]}"