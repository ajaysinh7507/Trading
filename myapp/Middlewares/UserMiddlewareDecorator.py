import jwt
from bson import ObjectId
from django.http import HttpResponseRedirect


def checkAuthLogin():
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            
            validateRequest = {
                "email":{
                    "required": True
                },
                "password":{
                    "required": True
                }
            }
            
            return view_func(request, *args, **kwargs)
        return wrap
    return decorator

def checkAddUser():
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            return view_func(request, *args, **kwargs)
        return wrap
    return decorator
