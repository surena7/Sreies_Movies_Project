from django.db import models
from django.contrib.auth.models import User
from web.models import Movies  



class Favorite(models.Model):
    user = models.ForeignKey(User,on_delete=models.CASCADE,related_name='favorites')
    movie = models.ForeignKey(Movies,on_delete=models.CASCADE,related_name='favorited_by')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ['user', 'movie']
        ordering = ['-created_at']
    
    def __str__(self):
        return f"{self.user.username} - {self.movie.title}"