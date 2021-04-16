from django.http  import JsonResponse
from django.views import View

from .models      import *

class MenuView(View):
    def get(self, request):
        try:
            menu_list = Menu.objects.all()
            results = []
            for menu in menu_list:
                main_category = menu.maincategory_set.all()
                main_list = []
                for main in main_category:
                    sub_category = main.subcategory_set.all()
                    sub_list = []
                    for sub in sub_category:
                        sub_pair = {"id" : sub.id, "name" : sub.name}
                        sub_list.append(sub_pair)
                    main_list.append(
                        {   
                            "id"           : main.id,
                            "name"         : main.name,
                            "sub_category" : sub_list
                        }
                    )
                results.append(
                    {
                        "id"            : menu.id,
                        "name"          : menu.name,
                        "main_category" : main_list
                    }
                )
            return JsonResponse({'results':results}, status=200)
        
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)


