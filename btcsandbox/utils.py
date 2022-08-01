import hashlib, random

from django.utils import timezone


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
    

def gen_two(number):
    number = str(number)

    if len(number) == 1:
        return f'0{number}'
    return number

def refcode():
    prefix = str(timezone.now().microsecond)[:4]
    render_year = str(timezone.now().year)[2:]
    render_month = str(gen_two(timezone.now().month))
    render_day = str(gen_two(timezone.now().day))
    render_hour = str(gen_two(timezone.now().hour))
    render_minute = str(gen_two(timezone.now().minute))
    render_second = str(gen_two(timezone.now().second))

    uci = render_year + render_month + render_day + render_hour + render_minute + render_second

    return f'{prefix}{uci}'