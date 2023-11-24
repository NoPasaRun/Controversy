from django.urls import path

from payment.views import payment_card, progress_payment, get_payment_status


app_name = "payment"


urlpatterns = [
    path("self/", payment_card, name="payment_self"),
    path("someone/", payment_card, name="payment_someone"),
    path("progress_payment/", progress_payment, name="progress_payment"),
    path("status/<uuid:payment_uid>/", get_payment_status, name="get_payment_status")
]