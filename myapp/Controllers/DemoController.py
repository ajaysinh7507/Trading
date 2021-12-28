import json
from django.http import HttpResponse
from django.shortcuts import render

from myapp.Utils.mongodb import get_db_handle, get_collection_handle
from myapp.Middlewares.AuthMiddlewareDecorator import isAuth
from myapp.Middlewares.UserMiddlewareDecorator import checkAddUser
class DemoController:
    
    @isAuth()
    def dashboard(request):
        user = request.auth
        
        return render(request, "index.html")

    @isAuth()
    @checkAddUser()
    def user(request):
        print(request)

        return HttpResponse(json.dumps({"status": True}), content_type='application/json')