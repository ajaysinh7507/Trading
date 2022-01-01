from django.contrib import admin
from django.urls import path,include
from .Controllers.DemoController import DemoController
from .Controllers.AuthController import AuthController
from .Controllers.KiteController import KiteController
from .Controllers.ScriptController import ScriptController

urlpatterns = [
    path('home', DemoController.dashboard, name="home"),
    path('login', AuthController.viewLogin, name="login"),
    path('auth-login', AuthController.authLogin, name="authLogin"),

    path('get-script-data', ScriptController.getAllScript, name="script.getAllScript"),
    path('get-historical-data', KiteController.getHistoricalData, name="kite.getHistoricalData"),
    path('kite-order-place', KiteController.orderPlace, name="kite.order.place"),
    
    path('add-user', DemoController.user, name="add.user")
]