import json
import re
import jwt

from django.http import JsonResponse

from my_settings  import SECRET_KEY, ALGORITHM
from users.models import User

def validate_phone_number(phone_number):
    phone_number_form = re.compile('^01([0|1|6|7|8|9]?)([0-9]{3,4})([0-9]{4})$')
    return phone_number_form.match(phone_number)

def validate_email(email):
    email_form = re.compile('^[a-zA-Z0-9+-_.]+@[a-z]+\.[a-z]+$')
    return email_form.match(email)

#최소 10자, 최소 하나의 문자 및 하나의 숫자
def validate_password(password):
    password_form = re.compile('^(?=.*[A-Za-z])(?=.*\d)(\S){10,}$')
    return password_form.match(password)

def login_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            token        = request.headers.get('Authorization', None)
            payload      = jwt.decode(token, SECRET_KEY['secret'], algorithms=ALGORITHM)
            user         = User.objects.get(id=payload['id'])
            request.user = user
            return func(self, request, *args, **kwargs)
        except jwt.exceptions.DecodeError:
            return JsonResponse({'MESSAGE':'INVALID_TOKEN'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=400)
    
    return wrapper
