
from django import forms

from django.contrib.auth.forms import UserCreationForm
from ecart.models import ecart
from django.contrib.auth.models import User

class UserForm(UserCreationForm):
    email = forms.EmailField(required=True)  

    class Meta:
        model = User
        fields = ["username", "email", "password1", "password2"] 




class LoginForm(forms.Form):
    username = forms.CharField(
        label="Username",
        widget=forms.TextInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your username"
        })
    )
    password = forms.CharField(
        label="Password",
        widget=forms.PasswordInput(attrs={
            "class": "form-control",
            "placeholder": "Enter your password",
            "autocomplete": "current-password"
        })
    )


class EcartForm(forms.ModelForm):
    class Meta:
        model = ecart
        fields = ["name", "picture", "price"]

class AddProductForm(forms.ModelForm):
    class Meta:
        model = ecart
        exclude = ["user"]

            

    
        