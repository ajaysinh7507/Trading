def loginSchema():
    validator_schema = {
                "username":{
                    "required": True
                },
                "password":{
                    "required": True,
                    "min": 8
                }
            }
    
    return validator_schema