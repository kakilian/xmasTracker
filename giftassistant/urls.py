from django.urls import path
from . import views

urlpatterns = [
    path("gift_assistant/", views.gift_assistant, name="gift_assistant"),
    path("save_gifts/", views.save_gift, name="save_gifts"),
]
