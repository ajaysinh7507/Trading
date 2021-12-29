import jwt
from bson import ObjectId
from django.http import HttpResponseRedirect

from myproject.settings import JWT_SECRET
from myapp.Models.User import User

def isAuth():
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            try:
                auth_token = request.COOKIES.get('authToken', '')
                
                if(auth_token and not auth_token == ""):
                    decoded_jwt = jwt.decode(auth_token, JWT_SECRET, algorithms=["HS256"])
                    auth_id = decoded_jwt['_id']
                   
                    
                    user = User.getOne({"_id": ObjectId(auth_id)})
                    
                    if user:
                        request.auth = user
                        
                        return view_func(request, *args, **kwargs)   
                    else:
                        response = HttpResponseRedirect('login')
                        response.delete_cookie("authToken")
                        
                        return response
                else:
                    response = HttpResponseRedirect('login')
                    response.delete_cookie("authToken")
                    
                    return response

            except Exception as e:
                response = HttpResponseRedirect('login')
                response.delete_cookie("authToken")
                
                return response
        return wrap
    return decorator
