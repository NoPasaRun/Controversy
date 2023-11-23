from django.shortcuts import render
from django.views.generic import TemplateView

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.translation import gettext_lazy as _
from django.views import View
from django.views.generic import ListView

from models import User
from server.forms import UserUpdateForm, UserForm


class AccountView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'profile': get_object_or_404(User, user=request.user)
        }
        return render(request, "user_app/account.html", context)


class LogIn(LoginView):
    template_name = "user_app/login.html"


class LogOut(LogoutView):
    pass


class SignUp(View):

    def get(self, request):
        user_form = UserForm()
        return render(
            request,
            'user_app/register.html',
            {"user_form": user_form, "profile_form": user_form}
        )

    def post(self, request):
        user_form = UserForm(request.POST)
        if user_form.is_valid() and user_form.is_valid():
            user = user_form.save()
            User(**user_form.cleaned_data).save()
            auth_user = authenticate(user=user, password=user_form["password1"])
            login(request=request, user=auth_user)
            return HttpResponseRedirect("/account/profile/", status=201)
        return render(
            request,
            'user_app/register.html',
            {"user_form": user_form, "profile_form": user_form}
        )


class UpdateProfileInfo(View, LoginRequiredMixin):

    def get(self, request):
        profile = get_object_or_404(User, pk=request.user.profile.id)
        template_name = "user_app/profile.html" if not request.htmx else "user_app/includes/profile_section.html"
        return render(request, template_name, {"profile": profile})

    def post(self, request):
        user = get_object_or_404(User, pk=request.user.profile.id)

        user_form = UserUpdateForm(request.POST)
        is_authenticated_by_email = True

        if user_form.is_valid():
            if user_form.cleaned_data.get("password1"):
                new_password = user_form.cleaned_data["password1"]
                user.set_password(new_password)
                user.save()
            return render(
                request,
                "user_app/profile.html",
                {"user": user, "updated": True}
            )
        is_authenticated_by_email = False
        return render(request,
                      "user_app/profile.html",
                      {
                          "user": user,
                          "errors": user_form.errors,
                          "is_authenticated_by_email": is_authenticated_by_email
                      }
        )


class Main(TemplateView):
    template_name = "cart/index.html"
