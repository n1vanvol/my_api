import bcrypt

def hash_password(password: str):
    hashed_password = bcrypt.hashpw(password=password.encode('utf-8'), salt=bcrypt.gensalt())
    return hashed_password.decode('utf-8')  

def verify_password(plain_password: str, hashed_password: str):
    return bcrypt.checkpw(plain_password.encode('utf-8'), hashed_password.encode('utf-8')) 