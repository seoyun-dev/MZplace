from django.http  import JsonResponse
from django.views import View
from django.db.models import Q

from places.models import Category, Place, FilterPlace, Filter, Course, CoursePlace
from hearts.models import Heart

###### cateogry - 카테고리별 장소 목록 페이지
# TODO signin_decorator 완료되면 heart 추가
class CategoryPlaceListView(View):
    def get(self, request, category_id):
        try: 
            category = Category.objects.get(id=category_id)
            offset   = int(request.GET.get('offset', 0))
            price    = request.GET.get('filter', '')

            q = Q()

            q |= Q(category__name = category.name)

            if price:
                q &= Q(place__price__contains = price)

            places      = Place.objects.filter(q).distinct()
            places_list = places[offset:offset+12]
            

            result = [
                {
                    'id'      : place.id,
                    'name'    : place.name,
                    'image_url' : place.image_url,
                    # 'heart': 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0
                }for place in places_list
            ]

            return JsonResponse(
                {
                    'result'               : result,
                    'total_places'          : places.count()
                }, status=200)
        
        except Category.DoesNotExist:
            return JsonResponse({'message':'CATEGORY_DOES_NOT_EXIST'}, status=404)




###### filter-places - 맞춤 필터 장소 목록 페이지
class CategoryPlaceListView(View):
    def get(self, request):
        try:
            main_category = request.GET.get('main_category', 'speakers')
            sub_category  = request.GET.get('sub_category')
            sort_method   = request.GET.get('sort_method', '-release_date')
            limit         = int(request.GET.get('limit', 9))
            offset        = int(request.GET.get('offset', 0))

            q = Q()

            if main_category:
                q &= Q(sub_category__category__name=main_category)

            elif sub_category:
                q &= Q(sub_category__name=sub_category)

            products      = Product.objects.filter(q).order_by(sort_method)
            products_list = products[offset:offset+limit]
            print(products_list[5].productimage_set.first().image_url)
            res_products = [
                {
                    'id'          : product.id,
                    'name'        : product.name,
                    'description' : product.description,
                    'price'       : product.price,
                    'image_url'   : [image.image_url for image in product.productimage_set.all()],
                    'release_date': product.release_date,
                } for product in products_list
            ]

            return JsonResponse({'RESULT':res_products, 'totalItems' : products.count()}, status=200)
        
        except Category.DoesNotExist:
            return JsonResponse({'message':'CATEGORY_DOES_NOT_EXIST'}, status=404)
        except SubCategory.DoesNotExist:
            return JsonResponse({'message':'SUB_CATEGORY_DOES_NOT_EXIST'}, status=404)



# ###### course<course_id> - 코스 상세 페이지
# class PlaceDetailView(View):
#     def get(self, request, product_id):
#         try:
#             product = Product.objects.get(id = product_id)
#             product_detail = {
#                 'id'           : product.id,
#                 'name'         : product.name,
#                 'product_image': [product.image_url for product in product.productimage_set.all()],
#                 'description'  : product.description,
#                 'content_url'  : product.content_url,
#                 'price'        : product.price,
#                 'stock'        : product.stock
#             }
#             return JsonResponse({"result" : product_detail}, status=200)
        
#         except Product.DoesNotExist:
#             return JsonResponse({"message" : "DoesNotExist"}, status=400)
        

# ###### place<place_id> - 장소 상세 페이지
# class PlaceDetailView(View):
#     def get(self, request, product_id):
#         try:
#             product = Product.objects.get(id = product_id)
#             product_detail = {
#                 'id'           : product.id,
#                 'name'         : product.name,
#                 'product_image': [product.image_url for product in product.productimage_set.all()],
#                 'description'  : product.description,
#                 'content_url'  : product.content_url,
#                 'price'        : product.price,
#                 'stock'        : product.stock
#             }
#             return JsonResponse({"result" : product_detail}, status=200)
        
#         except Product.DoesNotExist:
#             return JsonResponse({"message" : "DoesNotExist"}, status=400)



# ###### top-places - TOP 20 장소 목록 페이지

###### recommend-places - 찜기반 추천 장소 목록 페이지

###### distance-places - 거리별 추천 장소 목록 페이지

