from .views import Mainpage
from django.urls import path

urlpatterns = [
    path('', Mainpage.as_view(), name='mainpage'),
]