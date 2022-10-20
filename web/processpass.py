import bcrypt

def encryptpass(password):
    Password = password.encode('utf-8')
    salt = bcrypt.gensalt()
    Password = bcrypt.hashpw(Password, salt)
    return Password
