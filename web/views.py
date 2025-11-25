from django.shortcuts import render , get_object_or_404 , redirect
from .models import Movies , Category , Like
from django.db.models import Count
from Comment.forms import CommentForm
from Subscription.models import Subscription
from Comment.models import Comment
from blog.models import Post
from django.http import JsonResponse
from django.contrib.auth.decorators import login_required
from django.views.decorators.http import require_POST
from django.views.decorators.csrf import csrf_exempt
import logging
from django.db.models import Q
from .forms import MovieSearchForm
from django.urls import reverse
from django.utils.http import urlencode









def home(request):
    movie = Movies.objects.all()
    subscription = Subscription.objects.all()
    category = Category.objects.annotate(
        movie_count = Count("movies")
    )[0:8]
    popular_movies = Movies.objects.filter(movie_or_not="سنمایی").order_by("-likes")[0:8]
    popular_series = Movies.objects.filter(movie_or_not="سریال").order_by("-likes")[0:8]
    feature_movie = Movies.objects.filter(movie_or_not="سنمایی").order_by("-likes")[0:1]
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




def detail(request, movie_id):
    movie = get_object_or_404(Movies, id=movie_id)
    related_movie = Movies.objects.filter(category=movie.category).exclude(id=movie.id)[:4]

    # مدیریت کامنت‌ها
    comments = Comment.objects.filter(movie=movie, parent__isnull=True).order_by("-created")
    
    if request.method == "POST":
        print("POST request received")  # دیباگ
        print("POST data:", request.POST)  # دیباگ
        
        if request.user.is_authenticated:
            # بررسی اینکه آیا کامنت جدید ارسال شده
            if 'comment_text' in request.POST:
                comment_text = request.POST.get('comment_text')
                print(f"Comment text received: {comment_text}")  # دیباگ
                
                if comment_text and len(comment_text.strip()) >= 10:
                    try:
                        comment = Comment.objects.create(
                            user=request.user,
                            movie=movie,
                            text=comment_text.strip()
                        )
                        print(f"Comment created: {comment.id}")  # دیباگ
                        
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return JsonResponse({
                                'success': True,
                                'message': 'کامنت با موفقیت ثبت شد',
                                'comment_id': comment.id
                            })
                        # ریدایرکت برای درخواست‌های غیر AJAX
                        return redirect('web:detail', movie_id=movie_id)
                        
                    except Exception as e:
                        print(f"Error creating comment: {e}")  # دیباگ
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return JsonResponse({
                                'success': False,
                                'message': 'خطا در ثبت کامنت'
                            }, status=500)
                else:
                    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                        return JsonResponse({
                            'success': False,
                            'message': 'کامنت باید حداقل ۱۰ کاراکتر داشته باشد'
                        })
            
            # مدیریت پاسخ به کامنت
            elif 'reply_text' in request.POST:
                parent_id = request.POST.get('parent_id')
                reply_text = request.POST.get('reply_text')
                print(f"Reply received - parent: {parent_id}, text: {reply_text}")  # دیباگ
                
                if reply_text and len(reply_text.strip()) >= 10:
                    try:
                        parent_comment = Comment.objects.get(id=parent_id, movie=movie)
                        reply = Comment.objects.create(
                            user=request.user,
                            movie=movie,
                            text=reply_text.strip(),
                            parent=parent_comment
                        )
                        print(f"Reply created: {reply.id}")  # دیباگ
                        
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return JsonResponse({
                                'success': True,
                                'message': 'پاسخ با موفقیت ثبت شد',
                                'reply_id': reply.id
                            })
                        return redirect('web:detail', movie_id=movie_id)
                        
                    except Comment.DoesNotExist:
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return JsonResponse({
                                'success': False,
                                'message': 'کامنت اصلی یافت نشد'
                            })
                    except Exception as e:
                        print(f"Error creating reply: {e}")  # دیباگ
                        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                            return JsonResponse({
                                'success': False,
                                'message': 'خطا در ثبت پاسخ'
                            }, status=500)
        else:
            # کاربر لاگین نکرده
            if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
                return JsonResponse({
                    'success': False,
                    'message': 'لطفاً ابتدا وارد حساب کاربری خود شوید',
                    'login_required': True
                }, status=401)
            return redirect('account:login')

    is_liked = movie.is_liked_by_user(request.user) if request.user.is_authenticated else False

    return render(request, "web/detail.html", {
        "m": movie,
        "mr": related_movie,
        "comments": comments,
        "is_liked": is_liked,
    })
    


@require_POST
@login_required
def delete_comment(request, comment_id):
    try:
        comment = get_object_or_404(Comment, id=comment_id)
        print(f"Delete comment request - Comment: {comment.id}, User: {request.user.username}")
        
        # چک کردن permission
        if comment.user == request.user or request.user.is_staff:
            comment_id = comment.id
            comment.delete()
            print(f"Comment {comment_id} deleted successfully")
            
            return JsonResponse({
                'success': True,
                'message': 'کامنت با موفقیت حذف شد'
            })
        else:
            print("User not authorized to delete this comment")
            return JsonResponse({
                'success': False,
                'message': 'شما اجازه حذف این کامنت را ندارید'
            }, status=403)
            
    except Exception as e:
        print(f"Error deleting comment: {e}")
        return JsonResponse({
            'success': False,
            'message': 'خطا در حذف کامنت'
        }, status=500)
        
        
        
        
@require_POST
@login_required
def like_post(request, movie_id):
    try:
        print(f"Like request received for movie {movie_id} from user {request.user.username}")
        
        movie = get_object_or_404(Movies, id=movie_id)
        user = request.user
        
        # لاگ برای دیباگ
        print(f"Movie: {movie.name}, User: {user.username}")
        
        # بررسی آیا کاربر قبلاً لایک کرده یا نه
        like_exists = Like.objects.filter(user=user, movie=movie).exists()
        print(f"Like exists: {like_exists}")
        
        if like_exists:
            # حذف لایک
            Like.objects.filter(user=user, movie=movie).delete()
            movie.likes.remove(user)
            liked = False
            print("Like removed")
        else:
            # اضافه کردن لایک
            Like.objects.create(user=user, movie=movie)
            movie.likes.add(user)
            liked = True
            print("Like added")
        
        # به‌روزرسانی تعداد لایک‌ها
        total_likes = movie.total_likes()
        print(f"Total likes: {total_likes}")
        
        return JsonResponse({
            'liked': liked,
            'total_likes': total_likes,
            'success': True
        })
        
    except Exception as e:
        print(f"Error in like_post: {str(e)}")
        return JsonResponse({
            'error': 'خطا در پردازش درخواست',
            'success': False
        }, status=500)



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
    serieses = Movies.objects.filter(movie_or_not="سریال").order_by("-likes")
    return render(request,"web/popular_series.html",{"series":serieses})




def popular_movies_page(request):
    movies = Movies.objects.filter(movie_or_not="سنمایی").order_by("-likes")
    return render(request,"web/popular_movies.html",{"movie":movies})




def all_posts_page(request):
    a_post = Post.objects.all()
    return render(request,"web/all_posts.html",{"post":a_post})




def post_detail(request , post_id):
    post = Post.objects.get(id=post_id)
    return render(request,"web/post_detail.html",{"post":post})
    
    
    

def movie_search(request):
    if request.method == 'POST':
        form = MovieSearchForm(request.POST)
        if form.is_valid():
            search_query = form.cleaned_data['search_query']
            
            url = reverse('web:search_results')
            params = urlencode({'q': search_query})
            return redirect(f'{url}?{params}')
    
    else:
        form = MovieSearchForm()
    
    return render(request, 'web/search_page.html', {'form': form})


def search_results(request):
    search_query = request.GET.get('q', '').strip()
    print(f"Search query: '{search_query}'")  # برای دیباگ
    
    if search_query:
        movies = Movies.objects.filter(
            Q(name__icontains=search_query) | 
            Q(director__icontains=search_query) |
            Q(description__icontains=search_query) |
            Q(autor__icontains=search_query)
        ).distinct().order_by('-created_at')
        print(f"Found {movies.count()} movies")  # برای دیباگ
    else:
        movies = Movies.objects.none()
        print("No search query provided")  # برای دیباگ
    
    categories = Category.objects.all()
    
    context = {
        'movies': movies,
        'search_query': search_query,
        'results_count': movies.count(),
        'categories': categories
    }
    
    return render(request, 'web/search_result.html', context)