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

            Rate.objects.update_or_create(
                user       = request.user,
                product_id = data['product_id'],
                defaults   = {'rate':data['rate']})
            return JsonResponse({'MESSAGE': 'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse ({'MESSAGE': 'KEY_ERROR'}, status=400)

    def get(self,request):
        user_id    = request.GET.get('user')
        product_id = request.GET.get('product')

        rate = int(Rate.objects.get(user_id=user_id,product_id=product_id).rate)

        return JsonResponse({'results': rate}, status=200)