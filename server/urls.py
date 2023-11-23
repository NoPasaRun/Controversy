from django.urls import path

from server.views import Main

urlpatterns = [
    path("", Main.as_view(), name="index")
]
