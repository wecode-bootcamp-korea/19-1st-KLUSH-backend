import json

from django.views     import View
from django.http      import JsonResponse

from orders.models   import Cart, Order
from users.utils     import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data                = json.loads(request.body)
            user                = request.user
            quantity            = int(data['quantity'])
            product_id          = data['product_id']
            option_id           = data['option_id']
            current_quantity    = 0

            order, create = Order.objects.get_or_create(
                                    user            = user,
                                    order_status_id = 1
                                    )

            if Cart.objects.filter(order_id = order.id, product_id = product_id, option_id = option_id).exists():
                
                current_quantity = Cart.objects.get(order_id = order.id, product_id = product_id, option_id = option_id).quantity
                
            Cart.objects.update_or_create(
                    order_id   = order.id,
                    product_id = product_id,
                    option_id  = option_id,
                    defaults   = {
                        'quantity'    : current_quantity + quantity,
                        }
                    )
            
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        except JSONDecodeError:
            return JsonResponse({'MESSAGE':'JSON_DECODE_ERROR'}, status=400)

    @login_decorator
    def get(self, request):
        user = request.user

        order = Order.objects.get(user = user, order_status_id = 1)
        cart_lists = order.cart_set.all()

        carts = [{
            'product_name'      : carts.product.name,
            'sub_category_name' : carts.product.sub_category.name,
            'quantity'          : carts.quantity,
            'option'            : carts.option.weight,
            'image'             : carts.product.productimage_set.get(thumbnail_status = 1).image_url
            }for carts in cart_lists]

        return JsonResponse({'MESSAGE':'SUCCESS', 'results':carts}, status=200)

    @login_decorator
    def delete(self, request):
        data = json.loads(request.body)
        
        Cart.objects.get(
                product_id = data['product_id'], 
                option_id  = data['option_id']
                ).delete()
        
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
