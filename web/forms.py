from django import forms





class MovieSearchForm(forms.Form):
    search_query = forms.CharField(
        max_length=100,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'جستجوی فیلم یا کارگردان...',
            'dir': 'rtl'
        }),
        label=''
    )