from django.shortcuts import render
from .forms import SignUpForm
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect





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