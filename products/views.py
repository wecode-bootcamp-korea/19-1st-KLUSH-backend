from django.http import JsonResponse
from django.views import View

from .models import Menu, MainCategory, SubCategory, Product, ProductImage, ProductOption


class MenuView(View):
    def get(self, request):
        try:
            results = []
            main_category = MainCategory.objects.all()
            for main in main_category:
                sub_category = main.subcategory_set.all()
                sub_list = []
                for sub in sub_category:
                    sub_pair = {"id": sub.id, "name": sub.name}
                    sub_list.append(sub_pair)
                results.append(
                    {
                        "id": main.id,
                        "name": main.name,
                        "sub_category": sub_list
                    }
                )
            return JsonResponse({'results': results}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE': 'KEY_ERROR'}, status=400)

class MainProductView(View):
    def get(self, request):
        try:
            product_list = Product.objects.all()[:12]
            results = [
                {
                    "id"          : product.id,
                    "image_url"   : product.productimage_set.filter(thumbnail_status=True).first().image_url,
                    "name"        : product.name,
                    "description" : product.hashtag,
                    "price"       : float(product.price)
                } 
                for product in product_list
            ]
            
            return JsonResponse({'results' : results}, status=200)

        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)