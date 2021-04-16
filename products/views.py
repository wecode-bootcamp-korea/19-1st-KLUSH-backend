from django.http  import JsonResponse
from django.views import View

from .models      import Menu, MainCategory, SubCategory

class MenuView(View):
    def get(self, request):
        try:
            results = []
            
            menu_list = Menu.objects.all()
            menu_items = []
            for menu in menu_list:
                menu_items.append(
                    {
                        "id" : menu.id,
                        "name" : menu.name
                    }
                )
            
            main_list = MainCategory.objects.all()
            main_items = []
            for main in main_list:
                main_items.append(
                    {
                        "id" : main.id,
                        "name" : main.name
                    }
                )
            
            sub_list = SubCategory.objects.all()
            sub_items = []
            for sub in sub_list:
                sub_items.append(
                    {
                        "id" : sub.id,
                        "name" : sub.name
                    }
                )
            
            results.append(
                {
                    "menu"          : menu_items,
                    "main_category" : main_items,
                    "sub_category"  : sub_items
                }
            )

            return JsonResponse({'results':results}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
