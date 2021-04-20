import json

from django.views     import View
from django.http      import JsonResponse

from users.utils     import login_decorator
from .models         import Rate

class RateView(View):
    @login_decorator
    def post(self,request):
        try:
            data = json.loads(request.body)

            if rate := Rate.objects.filter(user=request.user,product_id=data['product_id']):
                rate.update(rate=data['rate'])
                return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

            Rate.objects.create(user=request.user,product_id=data['product_id'],rate=data['rate'])
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse ({'MESSAGE': 'KEY_ERROR'}, status=400)