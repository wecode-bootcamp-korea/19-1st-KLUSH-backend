from django.http      import JsonResponse
from django.views     import View
from django.db.models import Q

from .models import Menu, MainCategory, SubCategory, Product, ProductImage, ProductOption


class MenuView(View):
    def get(self, request):
        try:
            main_category = MainCategory.objects.all()
            results = [
                {
                    "id"             : main.id,
                    "name"           : main.name,
                    "sub_categories" : [{"id" : sub.id, "name" : sub.name} for sub in main.subcategory_set.all()]
                }
                for main in main_category
            ]
            
            return JsonResponse({'results':results}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

class ProductView(View):
    def get(self,request,product_id):
        if Product.objects.filter(id=product_id).exists():
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

            return JsonResponse({'results': product_informations}, status=200)
        return JsonResponse({'MESSAGE': 'NOT FOUND PRODUCT'}, status=404)

class MainProductView(View):
    def get(self, request):
        try:
            PRODUCT_COUNT = 12
            product_list = Product.objects.all()[:PRODUCT_COUNT]
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

class CategoryView(View):
    def get(self, request):
        try:
            main_category_id = request.GET.get('main_category_id')
            sub_category_id  = request.GET.get('sub_category_id')
            sort_type        = request.GET.get('sort')
            page             = request.GET.get('page')
            limit            = request.GET.get('limit')

            sort_list        = {
                "productPrice_asc"  : "price",
                "productPrice_desc" : "-price"
            }

            if page and limit:
                start        = (int(page) - 1) * int(limit)
                end          = int(page) * int(limit) 
                product_list = Product.objects.filter(Q(sub_category=sub_category_id)|
                                                      Q(main_category=main_category_id))[start : end]
            else:
                product_list = Product.objects.filter(Q(sub_category=sub_category_id)|
                                                      Q(main_category=main_category_id))

            if(sort_type is not None):
                product_list = product_list.order_by(sort_list[sort_type])

            results = [
                {
                    "id"          : product.id,
                    "image_url"   : product.productimage_set.filter(thumbnail_status=True).first().image_url,
                    "name"        : product.name,
                    "description" : product.hashtag,
                    "price"       : float(product.price), 
                    "label"       : [{"type" : label.name, "color" : label.color} for label in product.label_set.all()]
                }
                for product in product_list
            ]
            return JsonResponse({'results' : results}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

