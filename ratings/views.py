import json

from django.views     import View
from django.http      import JsonResponse

from users.utils     import login_decorator
from .models         import Rate, Comment, CommentImage
from products.models import Product

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

class CommentView(View):
    @login_decorator
    def post(self, request):
        try:
            data           = json.loads(request.body)
            user           = request.user
            content        = data['content']
            product_id     = data['product_id']
            image_url_list = data.get('image_urls', None)

            if not Product.objects.filter(id = product_id).exists():
                return JsonResponse({'MESSAGE':'PRODUCT_DOES_NOT_EXIST'}, status=404)

            if not content:
                return JsonResponse({'MESSAGE':'INSERT_CONTENT'}, status=400)

            comment, created = Comment.objects.update_or_create(
                    user       = user,
                    product_id = product_id,
                    defaults   = {'content':data['content']}
                    )
            if image_url_list:
                for image_url in image_url_list:
                    CommentImage.objects.create(
                            comment = comment,
                            image_url = image_url
                            )
            return JsonResponse({'MESSAGE':'SUCCESS'}, status=201)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE':'JSON_DECODE_ERROR'}, status=400)

    def get(self, request, product_id):
        if not Product.objects.filter(id = product_id).exists():
            return JsonResponse({'MESSAGE':'PRODUCT_DOES_NOT_EXIST'}, status=404)

        comment_list = [{
            'content' : comment_list.content,
            'image_url' : [image.image_url for image in comment_list.commentimage_set.all()],
            'created_at' : comment_list.created_at
            }for comment_list in Comment.objects.filter(product_id = product_id)]
        return JsonResponse({'MESSAGE':'SUCCESS', 'results':comment_list}, status=200)

    @login_decorator
    def delete(self, request):
        try:
            data       = json.loads(request.body)
            user       = request.user
            comment_id = data['comment_id']

            if not Comment.objects.filter(id = comment_id).exists():
                return JsonResponse({'MESSAGE':'COMMENT_DOES_NOT_EXIST'}, status=404)
       
            comment = Comment.objects.get(id = comment_id)
        
            if user != comment.user:
                return JsonResponse({'MESSAGE':'INVALID_USER'}, status=401)

            Comment.objects.get(id = comment_id).delete()

            return JsonResponse({'MESSAGE':'SUCCESS'}, status=200)
        except KeyError:
            return JsonResponse({'MESSAGE':'KEY_ERROR'}, status=400)
        except json.JSONDecodeError:
            return JsonResponse({'MESSAGE':'JSON_DECODE_ERROR'}, status=400)
