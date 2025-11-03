from django.db import models
from django.contrib.auth.models import User





class Category(models.Model):
    name = models.CharField(max_length=201 , verbose_name="نام دسته بندی")
    descriptions = models.TextField(verbose_name="توضیحات دسته یندی")
    image = models.ImageField(upload_to="cateimage/")
    def __str__(self):
        return self.name
    
    def get_movies_count(self):
        return self.movies_set.count()    

class Movies(models.Model):
    
    Status = (
        ("coming soon","به زودی"),
        ("not finished","درحال ساخت"),
        ("finished","اتمام ساخت"),
    )
    
    Movie = (
        ("سنمایی","Mo"),
        ("سریال","Se"),
    )
    
    name = models.CharField(max_length=201,verbose_name="نام")
    decriptions = models.TextField(verbose_name="توضیحات")
    status = models.CharField(max_length=201 , choices=Status , verbose_name="وضعیت فیلم")
    ep_number = models.PositiveIntegerField(default=1 , verbose_name="تعداد قسمت")
    season_number = models.PositiveIntegerField(default=1 , verbose_name="تعداد فصل")
    country = models.CharField(max_length=201 , verbose_name="کشور سازنده")
    pictrue = models.ImageField(upload_to="movie_pictrues/" , verbose_name="عکس فیلم")
    category = models.ForeignKey(Category,on_delete=models.CASCADE , verbose_name="ژانر")
    movie_or_not = models.CharField(max_length=201 , choices=Movie , verbose_name="سریال یا سینمایی")
    imdb_rate = models.DecimalField(max_digits=3 , decimal_places=1 , default=0.0 , verbose_name="نمره ی ای ام دی بی")
    autor = models.CharField(max_length=201 , verbose_name="نویسنده")
    director = models.CharField(max_length=201 , verbose_name="کاگردان")
    created_at = models.PositiveIntegerField(default=2001 , verbose_name="سال ساخت")
    like_counts = models.PositiveIntegerField(default=0 , verbose_name="تعداد لایک")
    def __str__(self):
        return self.name
    
    def is_liked_by_user(self , user):
        if user.is_authenticated :
            return self.like_set.filter(user=user).exists()
        return False
    

class Like(models.Model):
    user = models.ForeignKey(User , on_delete=models.CASCADE , verbose_name="کاربر")
    movie = models.ForeignKey(Movies , on_delete=models.CASCADE , verbose_name="فیلم")
    created = models.DateTimeField(auto_now_add=True , verbose_name="تاریخ ثبت")
    class Meta:
        unique_together = ("user","movie")
    
    def __str__(self):
        return f"{self.user.username} liked {self.movie.name} !"
      
