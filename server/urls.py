from django.urls import path

from server.views import Main, AccountView, LogIn, LogOut, SignUp, UpdateProfileInfo

urlpatterns = [
    path("", Main.as_view(), name="index"),
    path("account/", AccountView.as_view(), name="account"),
    path("login/", LogIn.as_view(), name="login"),
    path("logout/", LogOut.as_view(), name="logout"),
    path("register/", SignUp.as_view(), name="sign-up"),
    path("profile/", UpdateProfileInfo.as_view(), name="profile")
]
