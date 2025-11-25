from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.contrib.auth.decorators import login_required, user_passes_test
from django.shortcuts import render, get_object_or_404, redirect
from django.contrib import messages
from django.contrib.auth import get_user_model
from django.db.models import Count, Q
import datetime
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from .models import Favorite
from web.models import Movies



User = get_user_model()
 


def is_staff_user(user):
    return user.is_staff



# accounts/views.py - اضافه کردن ویوهای جدید

@login_required
def user_dashboard(request):
    """داشبورد کاربری عادی"""
    user = request.user
    
    # گرفتن لیست علاقه‌مندی‌ها (با فرض اینکه مدل Favorite دارید)
    try:
        favorites = user.favorites.all()[:10]  # آخرین 10 علاقه‌مندی
    except:
        favorites = []
    
    # گرفتن لیست تماشا شده‌ها (با فرض اینکه مدل WatchHistory دارید)
    try:
        watch_history = user.watch_history.all().order_by('-watched_at')[:10]
    except:
        watch_history = []
    
    # اطلاعات اشتراک کاربر
    subscription_info = {
        'is_active': hasattr(user, 'subscription') and user.subscription.is_active,
        'expiry_date': getattr(getattr(user, 'subscription', None), 'expiry_date', None),
        'plan_name': getattr(getattr(user, 'subscription', None), 'plan_name', 'رایگان')
    }
    
    context = {
        'favorites': favorites,
        'watch_history': watch_history,
        'subscription_info': subscription_info,
        'user': user
    }
    
    return render(request, 'accounts/user_dashboard.html', context)

@login_required
def favorites_list(request):
    """لیست کامل علاقه‌مندی‌های کاربر"""
    try:
        favorites = request.user.favorites.all()
    except:
        favorites = []
    
    return render(request, 'accounts/favorites_list.html', {'favorites': favorites})

@login_required
def watch_history_list(request):
    """لیست کامل تاریخچه تماشا"""
    try:
        watch_history = request.user.watch_history.all().order_by('-watched_at')
    except:
        watch_history = []
    
    return render(request, 'accounts/watch_history_list.html', {'watch_history': watch_history})

@login_required
def subscription_details(request):
    """جزییات اشتراک کاربر"""
    subscription = getattr(request.user, 'subscription', None)
    
    context = {
        'subscription': subscription,
        'has_subscription': subscription and subscription.is_active
    }
    
    return render(request, 'accounts/subscription_details.html', context)




@login_required
@user_passes_test(is_staff_user)
def admin_dashboard(request):
    """داشبورد ادمین برای مدیریت کاربران"""
    # آمار کاربران
    total_users = User.objects.count()
    active_users = User.objects.filter(is_active=True).count()
    staff_users = User.objects.filter(is_staff=True).count()
    superusers = User.objects.filter(is_superuser=True).count()
    
    # کاربران جدید امروز
    today = datetime.date.today()
    new_users_today = User.objects.filter(date_joined__date=today).count()
    
    # کاربران به تفکیک وضعیت
    users_by_status = User.objects.aggregate(
        active=Count('pk', filter=Q(is_active=True)),
        inactive=Count('pk', filter=Q(is_active=False)),
        staff=Count('pk', filter=Q(is_staff=True)),
    )
    
    # آخرین کاربران ثبت‌نام کرده
    recent_users = User.objects.all().order_by('-date_joined')[:10]
    
    context = {
        'total_users': total_users,
        'active_users': active_users,
        'staff_users': staff_users,
        'superusers': superusers,
        'new_users_today': new_users_today,
        'users_by_status': users_by_status,
        'recent_users': recent_users,
    }
    
    return render(request, 'accounts/admin_dashboard.html', context)




@login_required
@user_passes_test(is_staff_user)
def user_list(request):
    """لیست تمام کاربران"""
    users = User.objects.all().order_by('-date_joined')
    return render(request, 'accounts/user_list.html', {'users': users})




@login_required
@user_passes_test(is_staff_user)
def user_detail(request, user_id):
    """جزییات کاربر"""
    user = get_object_or_404(User, id=user_id)
    return render(request, 'accounts/user_detail.html', {'user': user})




@login_required
@user_passes_test(is_staff_user)
def toggle_user_active(request, user_id):
    """فعال/غیرفعال کردن کاربر"""
    user = get_object_or_404(User, id=user_id)
    
    if request.user != user:  # جلوگیری از غیرفعال کردن خود
        user.is_active = not user.is_active
        user.save()
        
        status = "فعال" if user.is_active else "غیرفعال"
        messages.success(request, f'کاربر {user.username} {status} شد.')
    else:
        messages.error(request, 'نمی‌توانید حساب خود را غیرفعال کنید.')
    
    return redirect('accounts:user_list')





def signup(request):
    template = "registration/signup.html"
    if request.method == "POST":
        form = SignUpForm(request.POST)
        if form.is_valid():
            if User.objects.filter(username=form.cleaned_data["username"]).exists():
                return render(request,template,{
                    "form":form,
                    "error_message":"UserName Is Already Exists !"
                })
            elif User.objects.filter(email=form.cleaned_data["email"]).exists():
                return render(request,template,{
                    "form":form,
                    "error_message":"Email Is Already Exists !"
                })
            elif form.cleaned_data["password1"]!=form.cleaned_data["password2"]:
                return render(request,template,{
                    "form":form,
                    "error_message":"The Passwords Is Not Match !"
                })
            else :
                user=User.objects.create_user(
                    form.cleaned_data["username"],
                    form.cleaned_data["email"],
                    form.cleaned_data["password1"],
                )
                user.save()
                return HttpResponseRedirect("login")
            
    else :
        form=SignUpForm()
            
    return render(request,template,{"form":form})






@login_required
@require_POST
def toggle_favorite(request, movie_id):
    """اضافه یا حذف از علاقه‌مندی‌ها (AJAX)"""
    try:
        movie = get_object_or_404(Movies, id=movie_id)
        
        favorite_exists = Favorite.objects.filter(user=request.user,movie=movie).exists()
        
        if favorite_exists:
            Favorite.objects.filter(user=request.user, movie=movie).delete()
            liked = Falsemessage = "از علاقه‌مندی‌ها حذف شد ❤️"
        else:
            Favorite.objects.create(user=request.user, movie=movie)
            liked = True
            message = "به علاقه‌مندی‌ها اضافه شد 💖"
        total_favorites = Favorite.objects.filter(movie=movie).count()
        
        user_favorites_count = Favorite.objects.filter(user=request.user).count()
        
        return JsonResponse({
            'success': True,
            'liked': liked,
            'total_favorites': total_favorites,
            'user_favorites_count': user_favorites_count,
            'message': message
        })
        
    except Exception as e:
        return JsonResponse({
            'success': False,
            'error': 'خطا در ثبت علاقه‌مندی'
        }, status=500)



@login_required
def favorites_list(request):
    favorites = Favorite.objects.filter(user=request.user).select_related('movie')
    

    print(f"User: {request.user}")
    print(f"Number of favorites: {favorites.count()}")
    for fav in favorites:
        print(f"Favorite ID: {fav.id}, Movie: {fav.movie.name if fav.movie else 'No movie'}")
    
    context = {
        'favorites': favorites
    }
    return render(request, 'accounts/favorites_list.html', context)




@login_required
@require_POST
def remove_favorite(request, favorite_id):
    try:
        favorite = Favorite.objects.get(id=favorite_id, user=request.user)
        movie_title = favorite.movie.name
        favorite.delete()
        
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': True,
                'message': f'"{movie_title}" از علاقه‌مندی‌ها حذف شد'
            })
        else:
            messages.success(request, f'"{movie_title}" از علاقه‌مندی‌ها حذف شد')
            return redirect('accounts:favorites_list')
            
    except Favorite.DoesNotExist:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': 'علاقه‌مندی یافت نشد'
            }, status=404)
        else:
            messages.error(request, 'علاقه‌مندی یافت نشد')
            return redirect('accounts:favorites_list')
    except Exception as e:
        if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
            return JsonResponse({
                'success': False,
                'error': 'خطا در حذف علاقه‌مندی'
            }, status=500)
        else:
            messages.error(request, 'خطا در حذف علاقه‌مندی')
            return redirect('accounts:favorites_list')