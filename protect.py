import hashlib

def protect(string, first=True):
    salt = "1asd;;|1::A21;'aASd11231aASdklkjllk1llk12l3jklff))DS001K1KL123"
    if first:
        string = hashlib.sha512(string).hexdigest()
    for x in range(100):
        string = hashlib.sha512(string+salt).hexdigest()

    return string
        
