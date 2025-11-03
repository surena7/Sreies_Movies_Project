from django.contrib import admin
from .models import Category , Movies




@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ["name"]
    

@admin.register(Movies)
class MovieAdmin(admin.ModelAdmin):
    list_display = ["name","status","category","director"]
    