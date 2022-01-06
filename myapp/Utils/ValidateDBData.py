def ValidateDBData(validator_schema, data):
    keys = data.keys() 
    error_messages = {}
    
    for key in keys:
        
        if not key in validator_schema.keys():
            error_messages.append({key: key+" is undefined."})
            continue
        else:
            print(data[key], validator_schema[key])
            if not isinstance(data[key], validator_schema[key]) :
                error_messages[key] = key+" is required.".capitalize()+" type : "+str(type(data[key]))
                                        
    if len(error_messages) > 0:
        return {"status": False, "error": error_messages}
    else:
        return {"status": True}