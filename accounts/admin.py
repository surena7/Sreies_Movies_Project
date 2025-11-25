from django.contrib import admin
from .models import Favorite



@admin.register(Favorite)
class FavoritesAdmin(admin.ModelAdmin):
    list_display=["user" , "movie" , "created_at"]
    list_filter=["created_at"]