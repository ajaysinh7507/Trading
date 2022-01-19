from django.contrib import admin
from django.urls import path,include
from myapp.Controllers.DemoController import DemoController
from myapp.Controllers.AuthController import AuthController
from myapp.Controllers.KiteController import KiteController
from myapp.Controllers.ScriptController import ScriptController

urlpatterns = [
    path('', DemoController.dashboard, name="index"),
    path('home', DemoController.dashboard, name="home"),
    path('dashboard/<int:instrument_token>', DemoController.homeDashboard, name="home.instrument_token"),
    path('login', AuthController.viewLogin, name="login"),
    path('auth-login', AuthController.authLogin, name="authLogin"),

    path('get-script-data', ScriptController.getScript, name="script.getScript"),
    path('get-historical-data/<int:script_instrument_token>', KiteController.getHistoricalData, name="kite.getHistoricalData"),
    path('kite-order-place', KiteController.orderPlace, name="kite.order.place"),
    path('kite-order-post-back', KiteController.orderPostBack, name="kite.order.post.back"),

    
    path('add-user', DemoController.user, name="add.user")
]