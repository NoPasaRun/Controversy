from django.urls import path

from server.views import Main, AccountView, LogIn, LogOut, SignUp, UpdateProfileInfo, CartView, add_to_cart, \
    delete_from_cart, remove_from_cart, change_cart, OrderView

urlpatterns = [
    path("", Main.as_view(), name="index"),
    path("account/", AccountView.as_view(), name="account"),
    path("account/login/", LogIn.as_view(), name="login"),
    path("account/logout/", LogOut.as_view(), name="logout"),
    path("account/register/", SignUp.as_view(), name="sign-up"),
    path("account/profile/", UpdateProfileInfo.as_view(), name="profile"),
    path('cart/', CartView.as_view(), name="cart"),
    path('add_to_cart/', add_to_cart, name="add_to_cart"),
    path('delete_from_cart/', delete_from_cart, name="delete_from_cart"),
    path('remove_from_cart/', remove_from_cart, name="remove_from_cart"),
    path('change_cart/', change_cart, name="change_cart"),
    path('order/', OrderView.as_view(), name="order")
]
