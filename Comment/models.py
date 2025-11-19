from django.db import models
from django.contrib.auth.models import User
from web.models import Movies

class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, verbose_name="کاربر")
    movie = models.ForeignKey(Movies, on_delete=models.CASCADE, verbose_name="فیلم")
    text = models.TextField(verbose_name="متن کامنت")
    created = models.DateTimeField(auto_now_add=True, verbose_name="تاریخ ایجاد")
    parent = models.ForeignKey('self', on_delete=models.CASCADE, null=True, blank=True, 
                              verbose_name="پاسخ به", related_name='replies')
    
    class Meta:
        verbose_name = "کامنت"
        verbose_name_plural = "کامنت‌ها"
        ordering = ['-created']
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.name}"
    
    def get_replies(self):
        return self.replies.all()