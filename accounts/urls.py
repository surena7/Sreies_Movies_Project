from django.urls import path
from .views import *


app_name="accounts"


urlpatterns = [
    path("",signup,name="signup"),
    path('dashboard/',user_dashboard, name='user_dashboard'),
    # path('profile/',profile, name='profile'),
    path('admin-dashboard/',admin_dashboard, name='admin_dashboard'),
    path('users/',user_list, name='user_list'),
    path('users/<int:user_id>/',user_detail, name='user_detail'),
    path('users/<int:user_id>/toggle-active/',toggle_user_active, name='toggle_user_active'),
    path('dashboard/',user_dashboard, name='user_dashboard'),
    path('watch-history/',watch_history_list, name='watch_history_list'),
    path('subscription/',subscription_details, name='subscription_details'),
    path('favorites/',favorites_list, name='favorites_list'),
    path('favorites/toggle/<int:movie_id>/',toggle_favorite, name='toggle_favorite'),
    path('favorites/remove/<int:favorite_id>/',remove_favorite, name='remove_favorite'),

]