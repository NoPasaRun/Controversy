from django import forms
from django.contrib.auth import get_user_model
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

from .models import User, Order


class OrderForm(forms.ModelForm):

    class Meta:
        model = Order
        exclude = ["user", "products", "status"]
        fields = "__all__"


class UserForm(forms.Form):

    username = forms.CharField(required=True)
    password1 = forms.CharField(required=True)
    password2 = forms.CharField(required=True)

    def clean_username(self):
        username = self.cleaned_data["username"]
        try:
            get_user_model().objects.get(username=username)
        except get_user_model().DoesNotExist:
            return username
        self.add_error("username", "Такой пользователь уже существует")

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        if password1 == password2:
            return cleaned_data
        self.add_error("password1", "Пароли не совпадают")


class UserUpdateForm(forms.Form):
    password1 = forms.CharField(widget=forms.PasswordInput(), required=False)
    password2 = forms.CharField(widget=forms.PasswordInput(), required=False)
    email = forms.EmailField()

    def clean(self):
        cleaned_data = super().clean()
        password1 = cleaned_data.get("password1")
        password2 = cleaned_data.get("password2")
        user = User.objects.filter(email=cleaned_data.get("username"))
        if user:
            if user[0].is_authenticated and password1 == "" == password2:
                return
        if not password1:
            raise forms.ValidationError(
                "Заполните поля для пароля!"
            )
        if password1 != password2:
            raise forms.ValidationError(
                "Пароли не совпадают!"
            )
        if len(password1) < 10:
            raise forms.ValidationError(
                "Пароль должен содержать больше 9 символов!"
            )
        if user:
            user = user[0]
            if not user.check_password(cleaned_data.get("password1")):
                raise forms.ValidationError(
                    "Неверный пароль!"
                )
