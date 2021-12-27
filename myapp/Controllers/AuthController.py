from django.shortcuts import redirect, render
from django.http import HttpResponse, HttpResponseRedirect
import numpy as np
import jwt
from myproject.settings import JWT_SECRET


from myapp.utils.mongodb import get_db_handle, get_collection_handle
from myapp.utils.bcrypt import checkHash

class AuthController:
    
    def viewLogin(request):
        
        return render(request, "login.html")

    def authLogin(request):
        
        if request.method == "POST":
            body = request.POST
            
            email = body.get('username')
            password = body.get('password')

            db_handle = get_db_handle()
            user = get_collection_handle(db_handle, "users")
            
            user = user.find_one({"email": email, 'status': True})

            if not user:
                return redirect('login')
                
            if checkHash(password, user['password']):
                encoded_jwt = jwt.encode({"_id": str(user['_id'])}, JWT_SECRET, algorithm="HS256")
                
                response = HttpResponseRedirect('home')
                response.set_cookie("authToken", encoded_jwt)
                
                return response
            else:
                print("in else")
                return redirect('login')
        else:
            return redirect('login')