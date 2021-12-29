import jwt
from django.http import HttpResponseRedirect
from django.shortcuts import redirect, render

from myproject.settings import JWT_SECRET
from myapp.Utils.bcrypt import checkHash

from myapp.Middlewares.AuthMiddlewareDecorator import isAuth
from myapp.Middlewares.RequestMiddlewareDecorator import validateRequestData

from myapp.Validation.UserValidation import loginSchema

import myapp.Models.User as UserClass
class AuthController:
    
    def viewLogin(request):
        session_error = {}
        if request.session.get('error'):
            session_error = request.session.get('error')
            del request.session['error']
            
        return render(request, "login.html", {'session_error': session_error})
    
    @validateRequestData(loginSchema(), 'login')
    def authLogin(request):
        
        if request.method == "POST":
            body = request.POST
            
            email = body.get('username')
            password = body.get('password')
            
            user = UserClass.User().getOne({"email": email, 'status': True})
            user = user["result"]
            
            if not user or not user["status"]:
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