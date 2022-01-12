from django.shortcuts import redirect
import jwt
from bson import ObjectId
from django.http import HttpResponseRedirect

from myproject.settings import JWT_SECRET
import myapp.Models.User as UserClass

def isAuth():
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            try:
                auth_token = request.COOKIES.get('authToken', '')
                
                if(auth_token and not auth_token == ""):
                    decoded_jwt = jwt.decode(auth_token, JWT_SECRET, algorithms=["HS256"])
                    auth_id = decoded_jwt['_id']
                   
                    user = UserClass.User().getOne({"_id": ObjectId(auth_id)})
                    user = user['result']
                    
                    if user and user['status']:
                        request.auth = user
                        
                        return view_func(request, *args, **kwargs)   
                    else:
                        response = redirect('login')
                        response.delete_cookie("authToken")
                        
                        return response
                else:
                    response = redirect('login')
                    response.delete_cookie("authToken")
                    
                    return response

            except Exception as e:
                response = redirect('login')
                response.delete_cookie("authToken")
                
                return response
        return wrap
    return decorator
