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


class ProductView(View):
    def get(self,request,product_id=None):
        if product_id:
            if Product.objects.filter(id=product_id).exists:
                product = Product.objects.get(id=product_id)

                product_informations = [{
                    'product_name'    : product.name,
                    'product_price'   : float(product.price),
                    'product_hashtag' : product.hashtag,
                    'product_thumbnail_image' : product.productimage_set.filter(thumbnail_status=1).get().image_url,
                    'product_image'   : [image.image_url for image in product.productimage_set.filter(thumbnail_status=0)],
                    'product_options' : [{'id'    : option.id,
                                    'weight'     : float(option.weight),
                                    'extra_cost' : float(option.extra_cost)
                                    }for option in ProductOption.objects.filter(product_id=product_id)],
                    }]

                return JsonResponse({'result': product_informations}, status=200)
        if not product_id:
            return JsonResponse({'MESSAGE': 'NOT FOUND PRODUCT'}, status=404)
