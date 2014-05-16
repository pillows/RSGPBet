import hashlib

def protect(string, first=True):
    salt = "JKgZEjP9NeiNdJbRSfCM"
    if first:
        string = hashlib.sha512(string).hexdigest()
    for x in range(100):
        string = hashlib.sha512(string+salt).hexdigest()

    return string
        
