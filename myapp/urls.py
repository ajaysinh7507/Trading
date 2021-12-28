from django.contrib import admin
from django.urls import path,include
from .Controllers.DemoController import DemoController
from .Controllers.AuthController import AuthController
from .Controllers.KiteController import KiteController

urlpatterns = [
    path('home', DemoController.dashboard, name="home"),
    path('login', AuthController.viewLogin, name="login"),
    path('auth-login', AuthController.authLogin, name="authLogin"),

    path('get-historical-data', KiteController.getHistoricalData, name="kite.getHistoricalData"),
    
    path('add-user', DemoController.user, name="add.user")
]