import json

from django.views     import View
from django.http      import JsonResponse

from orders.models   import Cart, Order
from products.models import Product, ProductOption
from users.utils     import login_decorator

class CartView(View):
    @login_decorator
    def post(self, request):
        try:
            data        = json.loads(request.body)
            user        = request.user
            quantity    = int(data['quantity'])
            product_id  = data['product_id']
            option_id   = data['option_id']
            
            order = Order.objects.get(user = user, order_status_id = 1)

            if Cart.objects.filter(order_id = order.id, product_id = product_id).exists():
                
                cart_lists = Cart.objects.get(order_id = order.id, product_id = product_id)
                
                cart_lists.quantity += quantity
                cart_lists.total_price = (
                        cart_lists.product.price + cart_lists.product.productoption_set.get(id=product_id).extra_cost
                        ) * cart_lists.quantity
                cart_lists.save()
                
                return JsonResponse({'MESSAGE':'SUCCESS_UPDATE_QUANTITY'}, status=201)
            
            total_price = (
                    Product.objects.get(id=product_id).price + ProductOption.objects.get(id=option_id).extra_cost
                    ) * quantity

            Cart.objects.create(
                    order_id    = order.id,
                    product_id  = product_id,
                    option_id   = option_id,
                    quantity    = quantity,
                    total_price = total_price
                    )

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)

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
        
        Cart.objects.get(product_id = data['product_id']).delete()
        
        return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
