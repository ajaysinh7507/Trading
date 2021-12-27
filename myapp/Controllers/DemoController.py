from django.shortcuts import render
from django.http import HttpResponse
import numpy as np

from myapp.MiddlewareDecorator import isAuth

from myapp.utils.mongodb import get_db_handle, get_collection_handle

class DemoController:
    
    @isAuth()
    def dashboard(request):
        user = request.auth
       
        return render(request, "index.html")

