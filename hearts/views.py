import json

from django.http     import JsonResponse
from django.views    import View

from users.utils     import signin_decorator
# # from products.models import Product

# class CartView(View):
#     @signin_decorator
#     def post(self, request):
#         try:
#             data     = json.loads(request.body)
#             quantity = data['quantity']
#             product  = Product.objects.get(id=data['product_id'])
            
#             cart, created = Cart.objects.get_or_create(
#                 defaults  = {'quantity' : quantity},
#                 product   = product,
#                 user      = request.user
#             )
#             if not created:
#                 cart.quantity += quantity
#                 cart.save()
#                 return JsonResponse({"message" : "CART_QUANTITY_CHANGED"}, status=200)
#             return JsonResponse({"message" : "PUT_IN_CART_SUCCESS"}, status=201)

#         except KeyError:
#             return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
#         except json.JSONDecodeError:
#             return JsonResponse({'message':'JSONDecodeError'}, status=404)

#     @signin_decorator
#     def get(self, request):
#         cart_products = [{
#             'id'          : cart.id,
#             'product_name': cart.product.name,
#             'quantity'    : cart.quantity,
#             'price'       : cart.product.price,
#             'images'      : [image.image_url for image in cart.product.productimage_set.all()]}
#             for cart in Cart.objects.filter(user=request.user)]
#         return JsonResponse({"message" : "SUCCESS", "cart" : cart_products}, status=200)
    
#     @signin_decorator
#     def delete(self, request):
#         try:
#             data = json.loads(request.body)
#             Cart.objects.filter(user=request.user, id__in=data['cart_ids']).delete()
#             return JsonResponse({"message":"DELETE_SUCCESS"}, status=200)

#         except json.JSONDecodeError:
#             return JsonResponse({'message':'JSONDecodeError'}, status=404)
        
#         except KeyError:
#             return JsonResponse({"message" : "KEY_ERROR"}, status=400)

#     @signin_decorator
#     def patch(self, request):
#         try: 
#             data         = json.loads(request.body)
#             cart_product = Cart.objects.get(user=request.user, id=data['cart_id'])
            
#             if cart_product.product.stock < cart_product.quantity + data['quantity']:
#                 return JsonResponse({"message" : "OUT_OF_STOCK"}, status=400)
            
#             cart_product.quantity += data['quantity']
#             cart_product.save()
#             return JsonResponse({"message" : "UPDATE_SUCCESS"}, status=200)

#         except KeyError:
#             return JsonResponse({"message" : "KEY_ERROR"}, status=400)

#         except Cart.DoesNotExist:
#             return JsonResponse({'message':'JSONDecodeError'}, status=404)