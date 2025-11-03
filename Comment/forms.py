from django import forms
from .models import Comment




class CommentForm(forms.ModelForm):
    class Meta:
       model=Comment
       fields = ["text"]
       widgets = {
           "Ttext":forms.Textarea(attrs={"class":"form-control" , "placeholder":"نظر خود را بنویسید" , "rows":3}),
       }