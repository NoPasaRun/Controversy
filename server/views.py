import json
from typing import Callable

from django.db import transaction
from django.urls import reverse
from django.views.generic import TemplateView

from django.contrib.auth import authenticate, login
from django.contrib.auth.mixins import LoginRequiredMixin
from django.contrib.auth.views import LoginView, LogoutView
from django.http import HttpResponseRedirect, JsonResponse, HttpResponse
from django.shortcuts import get_object_or_404, render
from django.views import View

from server.models import User, Product, Order
from server.forms import UserUpdateForm, UserForm, OrderForm
from server.cart import Cart


class AccountView(LoginRequiredMixin, View):

    def get(self, request):
        context = {
            'user': get_object_or_404(User, username=request.user.username)
        }
        return render(request, "user_app/account.html", context)


class LogIn(LoginView):
    template_name = "user_app/login.html"


class LogOut(LogoutView):
    pass


class SignUp(View):

    def get(self, request):
        return render(
            request,
            'user_app/register.html'
        )

    def post(self, request):
        user_form = UserForm(request.POST)
        if user_form.is_valid():
            username, password = user_form.cleaned_data["username"], user_form.cleaned_data["password1"]
            user = User(username=username)
            user.set_password(password)
            user.save()
            auth_user = authenticate(user=user, password=password)
            login(request=request, user=auth_user)
            return HttpResponseRedirect(reverse("account"))
        errors = list(map(lambda item: item[0], user_form.errors.values()))
        return render(
            request,
            'user_app/register.html',
            {"user_form": user_form, "errors": errors}
        )


class UpdateProfileInfo(View, LoginRequiredMixin):

    def get(self, request):
        user = get_object_or_404(User, pk=request.user.id)
        template_name = "user_app/profile.html"
        return render(request, template_name, {"user": user})

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

    extra_context = {"products": Product.objects.all()}


def redirect_to(func: Callable):
    def wrapper(request):
        cart = func(request)
        previous_abs_url = request.META.get('HTTP_REFERER')
        if previous_abs_url:
            if request.headers.get('x-requested-with'):
                return JsonResponse({"total_sum": cart.get_total_sum(), "cart": json.dumps(cart.cart)})
            return HttpResponseRedirect(previous_abs_url)
        return cart.serialize_data()

    return wrapper


class MainView(TemplateView):
    """
    Главная страница
    """

    template_name = 'cart/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        popular_products = Product.objects.all()[:8]

        context.update(
            {
                'popular_products': popular_products
            },
        )
        return context


def change_cart(request):
    if request.method == "GET":
        product_id = request.GET["product_id"]
        product = Product.objects.filter(id=product_id).first()
        if product:
            with transaction.atomic():
                delete_from_cart(request)
                get_data = request.GET.copy()
                get_data["product_id"] = str(product.id)
                request.GET = get_data
                add_to_cart(request)
        return HttpResponseRedirect("/cart/")


@redirect_to
def add_to_cart(request):
    if request.method == "GET":
        cart = Cart(request.session)
        product_id = request.GET.get("product_id")
        if product_id:
            amount = request.GET.get("amount", 1)
            cart.add(product_id, int(amount))
        return cart


def delete_from_cart(request):
    if request.method == "GET":
        product_id = request.GET["product_id"]
        cart = Cart(request.session)
        cart.__delitem__(product_id)
        return HttpResponseRedirect("/cart/")


@redirect_to
def remove_from_cart(request):
    if request.method == "GET":
        cart = Cart(request.session)
        product_id = request.GET.get("product_id")
        if product_id:
            amount = request.GET.get("amount", -1)
            cart.add(product_id, int(amount))
        return cart


class CartView(View):
    def get(self, request):
        cart = Cart(request.session)
        cart_data = cart.serialize_data()
        return render(
            request,
            "cart/cart.html",
            {"cart": cart_data, "total_price": cart.get_total_sum()}
        )


def no_cart_main_page(function):
    def wrapper(self, request):
        cart = Cart(request.session)
        if cart.cart:
            return function(self, request)
        return HttpResponseRedirect("/")

    return wrapper


def no_cart_decorator(cls):
    def wrapper():
        for function_name in ["get", "post"]:
            method = getattr(cls, function_name)
            new_method = no_cart_main_page(method)
            setattr(cls, function_name, new_method)
        return cls

    return wrapper()


@no_cart_decorator
class OrderView(View):

    def get(self, request):
        cart = Cart(request.session)
        cart_data = cart.serialize_data()
        return render(
            request, "cart/order.html",
            {"cart": cart_data, "total_price": cart.get_total_sum(),
             "payment_types": Order.PAYMENT_TYPES}
        )

    def post(self, request):

        cart = Cart(request.session)
        request.POST = request.POST.copy()
        user = request.user

        if request.POST.get("phone"):
            request.POST["phone"] = request.POST["phone"].replace("+7", "")
            request.POST["phone"] = "".join([sym for sym in request.POST["phone"] if sym.isdigit()])

        if not User.objects.filter(username=request.POST.get("username")) or not user.is_authenticated:

            user_form = UserForm(request.POST)

            if user_form.is_valid():
                user, created = User.objects.get_or_create(username=user_form.cleaned_data["username"])
                if created:
                    password = user_form.cleaned_data["password1"]
                    user.set_password(password)
                    user.save()
            else:
                cart_data = cart.serialize_data()
                return render(request, "cart/order.html", {"cart": cart_data,
                                                           "total_price": cart.get_total_sum(),
                                                           "errors": user_form.errors,
                                                           "payment_types": Order.PAYMENT_TYPES})
        order_form = OrderForm(request.POST)
        if order_form.is_valid():
            with transaction.atomic():
                order = Order.objects.create(user=user, **order_form.cleaned_data)
                for product in Product.objects.filter(id__in=[int(_id) for _id in cart.cart]):
                    order.products.add(product)
                cart.__delete__()
            redirect_path = '/payment/self' if order.payment_type == 'cart' else '/payment/someone'
            return HttpResponseRedirect(redirect_path)
        return HttpResponse(order_form.errors, status=500)
