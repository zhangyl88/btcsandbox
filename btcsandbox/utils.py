import hashlib, random

from account.models import Account


### key variables
emails                          = [i.email for i in Account.objects.all()]


### lambdas
encode_value                    = lambda value: str(value).encode('utf-8')

# Generate username from id
generate_username               = lambda id: hashlib.shake_256(encode_value(id)).hexdigest(6).lower()

# One Time Pin Code Generator
otp_gen                         = lambda : random.randint(100000, 999999)

# Two Factor Code Generator
tfa_gen                         = lambda : random.randint(10000, 99999)

# Search through a list of items
search_list                     = lambda item, list: True if item in list else False


### functions
def set_username(username, model):
    model.username = username
    model.save()

def set_email(email, model):
    model.email = email
    model.save()