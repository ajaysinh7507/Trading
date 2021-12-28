from django.http import HttpResponse, HttpResponseRedirect
import jwt

from myapp.Utils.mongodb import get_db_handle, get_collection_handle
from myproject.settings import JWT_SECRET

class AuthMiddleware:
    
    def __init__(self, get_response):
        self.get_response = get_response
        # One-time configuration and initialization.

    def __call__(self, request):
        # Code to be executed for each request before
        # the view (and later middleware) are called.

        response = self.get_response(request)

        # Code to be executed for each request/response after
        # the view is called.

        return response
    
    def process_view(self, request, view_func, view_args, view_kwargs):
        
        auth_token = request.COOKIES.get('authToken', '')

        print("print",request,view_func,view_args, view_kwargs)
        
        if(auth_token and not auth_token == ""):
            decoded_jwt = jwt.decode(auth_token, JWT_SECRET, algorithms=["HS256"])
            auth_id = decoded_jwt['_id']
            
            db_handle = get_db_handle()
            user = get_collection_handle(db_handle, "users")
            
            user = user.find_one({"_id": auth_id, 'status': True})

            if user:
                request.auth = user
                
            else:
                return HttpResponseRedirect('login')
        else:
            return HttpResponseRedirect('login')
            
