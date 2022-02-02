from .models import Author
from django import forms


class AuthorForm(forms.ModelForm):
    class Meta:
        model = Author
        fields = '__all__'
