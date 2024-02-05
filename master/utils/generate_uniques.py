import string
import random 

def generate_password(digits=8):
    """
    This function will genrate unique password with given digits

    Bydefault will generate 8 digits password
    """
    chs = string.ascii_letters + string.digits + '@_$.'
    password_ = ''
    for d in range(0, digits):
        password_ +=  chs[random.randint(0, len(chs) - 1)]
    return password_

def generate_otp(digits=6):
    """
    This function will genrate otp for 6/4 digits by default.
    """
    if digits == 6:
        otp_ = random.randint(111111, 999999)
    return otp_
