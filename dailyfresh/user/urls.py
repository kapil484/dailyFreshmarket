"""dailyfresh URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls.static import static
from django.conf import settings
from django.urls import path
from . import views

app_name='user'
urlpatterns = [
    path('register/', views.register,name='register'),
    path('register_handle/', views.register_handle),
    path('register_exist/', views.register_exist),
    path('login_handle/', views.login_handle),
    path('login/', views.login),
    path('info/', views.info),
    #url(r'^order/', views.order),
    path('site/', views.site),
    path('logout/', views.logout),
    path('user_center_order/', views.user_center_order),
]
urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
