from django.http import JsonResponse
from django.views import View

from .models import Menu, MainCategory, SubCategory, Product, ProductImage, ProductOption


class MenuView(View):
    def get(self, request):
        try:
            main_category = MainCategory.objects.all()
            results = [
                {
                    "id" : main.id,
                    "name" : main.name,
                    "sub_categories" : [{"id" : sub.id, "name" : sub.name} for sub in main.subcategory_set.all()]
                }
                for main in main_category
            ]
            
            return JsonResponse({'results':results}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)