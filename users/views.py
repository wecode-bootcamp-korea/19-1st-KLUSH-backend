import json
import bcrypt
import jwt

from django.http            import JsonResponse
from django.views           import View
from django.db.models       import Q

from .utils        import validate_phone_number, validate_email, validate_password
from my_settings   import ALGORITHM, SECRET_KEY
from users.models  import User
from orders.models import Order, OrderStatus

class SignUpView(View):
    def post(self, request):
        try:
            data         = json.loads(request.body)
            name         = data['name']
            phone_number = data['phone_number']
            email        = data['email']
            nickname     = data.get('nickname', None)
            password     = data['password']

            if not validate_phone_number(phone_number):
                return JsonResponse({'MESSAGE':'INVALID_MOBILE_NUMBER'}, status=400)
            
            if not validate_email(email):
                return JsonResponse({'MESSAGE':'INVALID_EMAIL'}, status=400)

            if not validate_password(password):
                return JsonResponse({'MESSAGE':'INVALID_PASSWORD'}, status=400)

            if User.objects.filter(
                    Q(phone_number = phone_number) |
                    Q(email = email) 
                    ).exists():
                return JsonResponse({'MESSAGE':'ALREADY_EXISTS'}, status=400)

            password        = data['password'].encode('utf-8')
            hashed_password = bcrypt.hashpw(password, bcrypt.gensalt())
            hashed_password = hashed_password.decode('utf-8')

            user = User.objects.create(
                    name         = name,
                    phone_number = phone_number,
                    email        = email,
                    nickname     = nickname,
                    password     = hashed_password
                    )

            Order.objects.create(
                    user         = user, 
                    order_status = OrderStatus.objects.get(status=0)
                    )

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

class SignInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            login_id = data['login_id']
            password = data['password']

            if user := User.objects.filter(
                    Q(email        = login_id) |
                    Q(account_name = login_id)
                    ):
                
                if bcrypt.checkpw(password.encode('utf-8'), user.get().password.encode('utf-8')):
                    token = jwt.encode({'id' : user.get().id}, SECRET_KEY['secret'], algorithm=ALGORITHM)
                    return JsonResponse({'MESSAGE':'SUCCESS', 'TOKEN':token}, status=200)
                return JsonResponse({'MESSAGE':'PASSWORD_ERROR'}, status=401)
            return JsonResponse({'MESSAGE':'INVALID_USER'}, status=404)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
