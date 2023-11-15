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
            page     = int(request.GET.get('page'))
            price    = request.GET.get('price')

            q = Q()

            q &= Q(category__name = category.name)

            if price:
                if price == 'pay':
                    price = '유료'
                    q &= Q(price__icontains = price)
                elif price == 'free':
                    price = '무료'
                    q &= Q(price__icontains = price)
                else:
                    return JsonResponse({'message':'CHECK_PRICE'}, status=404)

            places      = Place.objects.filter(q).distinct()
            places_list = places[12*(page-1):12*page]
            
            result = [
                {
                    'id'       : place.id,
                    'name'     : place.name,
                    'image_url': place.image_url,
                    # TODO heart 구현
                    # 'heart'    : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0
                }for place in places_list
            ]

            return JsonResponse(
                {
                    'message'     : 'SUCCESS',
                    'result'      : result,
                    'total_places': places.count()
                }, status=200)
        
        except Category.DoesNotExist:
            return JsonResponse({'message':'CATEGORY_DOES_NOT_EXIST'}, status=404)




###### filter - 맞춤 필터 장소 목록 페이지
class FilterPlaceListView(View):
    def get(self, request):
        price     = request.GET.get('price')
        filters   = request.GET.get('filters')
        districts = request.GET.get('districts')
        page      = int(request.GET.get('page'))

        q = Q()

        if price:
            if price == 'pay':
                price = '유료'
                q &= Q(price__icontains = price)
            elif price == 'free':
                price = '무료'
                q &= Q(price__icontains = price)
            else:
                return JsonResponse({'message':'CHECK_PRICE'}, status=404)
        
        sub_filter_q = Q()
        if filters:
            filters = filters.split(',')
            for filter in filters:
                filter = int(filter)
                if filter in [1,2,3,4,5,6,7]:
                    sub_filter_q |= Q(filterplace__filter__id = filter)
                else:
                    return JsonResponse({'message':'CHECK_FILTER_ID'}, status=404)
        q &= sub_filter_q

        sub_district_q = Q()
        if districts:
            districts = districts.split(',')
            for district in districts:
                sub_district_q |= Q(district__icontains = district)
        q &= sub_district_q

        places      = Place.objects.filter(q)
        places_list = places[12*(page-1):12*page]

        result = [
            {
                'id'       : place.id,
                'name'     : place.name,
                'image_url': place.image_url,
                # TODO heart 구현
                # 'heart'    : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0,
                # 'price'    : place.price,
                # 'filter'   : [filter.name for filter in Filter.objects.filter(filterplace__place__id=place.id)],
                # 'district' : place.district,
            } for place in places_list
        ]

        return JsonResponse(
            {
                'message'   : 'SUCCESS',
                'result'    : result,
                'totalItems': places.count()
                }, status=200)
                



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

