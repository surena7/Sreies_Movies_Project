from django.shortcuts import render
from .models import Movies , Category , Like
from django.db.models import Count
from Comment.forms import CommentForm
from Subscription.models import Subscription
from Comment.models import Comment
from blog.models import Post





def home(request):
    movie = Movies.objects.all()
    subscription = Subscription.objects.all()
    category = Category.objects.annotate(
        movie_count = Count("movies")
    )[0:8]
    popular_movies = Movies.objects.filter(movie_or_not="سنمایی").order_by("-like_counts")[0:8]
    popular_series = Movies.objects.filter(movie_or_not="سریال").order_by("-like_counts")[0:8]
    feature_movie = Movies.objects.filter(movie_or_not="سنمایی").order_by("-like_counts")[0:1]
    comment = Comment.objects.all()
    blog = Post.objects.all().order_by("-created")
    return render(request,"web/home.html",{"movie":movie,
                                           "fe":feature_movie,
                                           "ps":popular_series,
                                           "pm":popular_movies,
                                           "cate":category,
                                           "su":subscription,
                                           "co":comment,
                                           "blog":blog,
                                           })




def detail(request , movie_id):
    movie = Movies.objects.get(id=movie_id)
    related_movie = Movies.objects.filter(category=movie.category).exclude(id=movie.id)[0:4]
    is_liked = False
    if request.user.is_authenticated :
        is_liked = movie.is_liked_by_user(request.user)
    form = CommentForm()
    comment = Comment.objects.filter(movie=movie).order_by("-created")
    return render(request,"web/detail.html",{"m":movie,"mr":related_movie,"is_liked":is_liked,"form":form,"comment":comment})




def all_movies(request):
    movie = Movies.objects.all()
    return render(request,"web/all.html",{"movie":movie})




def category_page(request , category_id):
    category = Category.objects.get(id=category_id)
    category_page = Movies.objects.filter(category=category)
    return render(request,"web/category.html",{"ct":category_page})




def most_viewes_page(request):
    movie = Movies.objects.all()




def popular_serieses_page(request):
    serieses = Movies.objects.filter(movie_or_not="سریال").order_by("-like_counts")
    return render(request,"web/popular_series.html",{"series":serieses})




def popular_movies_page(request):
    movies = Movies.objects.filter(movie_or_not="سنمایی").order_by("-like_counts")
    return render(request,"web/popular_movies.html",{"movie":movies})




def all_posts_page(request):
    a_post = Post.objects.all()
    return render(request,"web/all_posts.html",{"post":a_post})




def post_detail(request , post_id):
    post = Post.objects.get(id=post_id)
    return render(request,"web/post_detail.html",{"post":post})
    