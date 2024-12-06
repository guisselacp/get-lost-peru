from . import views
from django.urls import path, include

urlpatterns = [
    path('', views.userprofile, name='userprofile'),
    path('blog/', include('blog.urls')),
    path('mainpage/',include('mainpage.urls')),
    path('mainpage/', include('django.contrib.auth.urls')),
]

