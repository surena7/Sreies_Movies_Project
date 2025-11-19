from django.urls import path
from .views import *

app_name = "web"

urlpatterns = [
    path("", home, name="home"),
    path("movie/<int:movie_id>/", detail, name="detail"),  # حتماً name="detail"
    path("all-movies/", all_movies, name="all"),
    path("category/<int:category_id>/", category_page, name="category"),
    path("popular_series/", popular_serieses_page, name="popular_series"),
    path("popular_movies/", popular_movies_page, name="popular_movies"),
    path("app_posts/", all_posts_page, name="post_blog"),
    path("post_detail/<int:post_id>/", post_detail, name="post_detail"),
    path('like/<int:movie_id>/', like_post, name='like_post'),
    path("comment/delete/<int:comment_id>/",delete_comment, name="delete_comment"),
]