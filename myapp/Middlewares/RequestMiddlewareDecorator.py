from django.http import HttpResponseRedirect
from django.urls import reverse

def validateRequestData(validator_schema, redirect):
    def decorator(view_func):
        def wrap(request, *args, **kwargs):
            try:
                auth_fields = ["csrfmiddlewaretoken"]
                keys = dict(request.POST).keys() if request.method == "POST" else dict(request.GET).keys()
                body = request.POST if request.method == "POST" else request.GET
                
                error_messages = {}
                for key in keys:
                        if key in auth_fields:
                                continue
                        if not key in validator_schema.keys():
                                error_messages[key] = key+" is undefined."
                                continue
                        else:
                                if "required" in validator_schema[key]:
                                        if validator_schema[key]["required"]:
                                                if(str(body[key]).strip() == ""):
                                                        error_messages[key] = key+" is required.".capitalize()
                                                        continue
                                if "min" in validator_schema[key]:
                                        if(len(body[key]) < validator_schema[key]["min"]):
                                                error_messages[key] = "Minimum "+str(validator_schema[key]["min"])+" character long value required".capitalize()
                                                continue
                                if "max" in validator_schema[key]:
                                        if(len(body[key]) < validator_schema[key]["max"]):
                                                error_messages[key] = "Maximum "+str(validator_schema[key]["max"])+" character long value is valid".capitalize()
                                                continue

                if len(error_messages) > 0:
                        request.session['error'] = error_messages
                        return HttpResponseRedirect(redirect)
                else:
                    return view_func(request, *args, **kwargs)
            
            except Exception as e:
                    print(e)
                    return HttpResponseRedirect(reverse(redirect, args=({"status": False, "error": "There is issue with some value"},)))
            
        return wrap
    return decorator
