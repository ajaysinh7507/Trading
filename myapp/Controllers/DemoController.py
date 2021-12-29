import json
from django.http import HttpResponse
from django.shortcuts import render

from myapp.Middlewares.AuthMiddlewareDecorator import isAuth
class DemoController:
    
    @isAuth()
    def dashboard(request):
        user = request.auth
        
        return render(request, "index.html")

    @isAuth()
    def user(request):
        print(request)

        return HttpResponse(json.dumps({"status": True}), content_type='application/json')