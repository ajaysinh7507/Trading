def validator(valdatro_schema, body):
    
        keys = dict(body.POST).keys() if body.method == "POST" else dict(body.GET).keys()
        
        
