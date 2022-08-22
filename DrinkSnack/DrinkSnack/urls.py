"""DrinkSnack URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.0/topics/http/urls/
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
from atexit import register
from django.contrib import admin
from django.urls import path
from DrinkSnackApp.views import DrinkSnack

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', DrinkSnack.login , name="login"),
    path('register/',DrinkSnack.register,name="register"),
    path('default/',DrinkSnack.default,name="default"),
    path('wallet/',DrinkSnack.wallet,name="wallet"),
    path('orderconfirm/',DrinkSnack.order,name="order"),
    path('orderplaced/',DrinkSnack.orderplaced,name="orderplaced"),
    path('adminn/',DrinkSnack.adminn,name="adminn"),
    
]
