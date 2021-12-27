import bcrypt

def hash(password=""):
    try:
        password = password.encode('UTF-8')
        salt = bcrypt.gensalt()
        hashed = bcrypt.hashpw(password,salt)

        return hashed
    except Exception as e:
        print(e)
        return False

def checkHash(plainPassword, hashedPassword):
    try:
        plainPassword = plainPassword.encode('utf-8')
        hashedPassword = hashedPassword.encode('utf-8')
        
        if bcrypt.checkpw(plainPassword, hashedPassword):
            return True
        else:
            return False
    except Exception as e:
        print(e)
        return False   
