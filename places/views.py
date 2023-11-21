from django.http  import JsonResponse
from django.views import View
from django.db.models import Q

from places.models import Category, Place, FilterPlace, Filter, Course, CoursePlace
from hearts.models import Heart
from users.utils   import signin_decorator


###### cateogry - 카테고리별 장소 목록 페이지
class CategoryPlaceListView(View):
    @signin_decorator
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
                    return JsonResponse({'message':'CHECK_PRICE'}, status=400)

            places      = Place.objects.filter(q).distinct()
            places_list = places[12*(page-1):12*page]
            
            result = [
                {
                    'id'       : place.id,
                    'name'     : place.name,
                    'image_url': place.image_url,
                    # TODO heart 구현
                    # 'heart'    : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0 if not request.user else 0
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



####### courses - 코스 목록 페이지
class CourseListView(View):
    @signin_decorator
    def get(self, request):
        page     = int(request.GET.get('page'))
        price    = request.GET.get('price')

        q = Q()

        if price:
            if price == 'pay':
                price = '유료'
                q &= Q(price__icontains = price)
            elif price == 'free':
                price = '무료'
                q &= Q(price__icontains = price)
            else:
                return JsonResponse({'message':'CHECK_PRICE'}, status=400)

        courses      = Course.objects.filter(q).distinct()
        courses_list = courses[12*(page-1):12*page]
        
        result = [
            {
                'id'           : course.id,
                'name'         : course.name,
                'duration_time': course.duration_time,
                'price'        : course.price,
                'image_url'    : course.image_url,
                # TODO heart 구현
                # 'heart'    : 1 if Heart.objects.filter(course__id=course.id).filter(user=request.user) else 0 if not request.user else 0
            }for course in courses_list
        ]

        return JsonResponse(
            {
                'message'     : 'SUCCESS',
                'result'      : result,
                'total_places': courses.count()
            }, status=200)



###### filter - 맞춤 필터 장소 목록 페이지
class FilterPlaceListView(View):
    @signin_decorator
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
                return JsonResponse({'message':'CHECK_PRICE'}, status=400)
        
        sub_filter_q = Q()
        if filters:
            filters = filters.split(',')
            for filter in filters:
                filter = int(filter)
                if filter in [1,2,3,4,5,6,7]:
                    sub_filter_q |= Q(filterplace__filter__id = filter)
                else:
                    return JsonResponse({'message':'CHECK_FILTER_ID'}, status=400)
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
                # 'heart'    : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0 if not request.user else 0,
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
class CourseDetailView(View):
    @signin_decorator
    def get(self, request, course_id):
        try:
            course = Course.objects.get(id = course_id)
            course_detail = {
                'id'           : course.id,
                'name'         : course.name,
                'duration_time': course.duration_time,
                'price'        : course.price,
                'image_url'    : course.image_url,
                # TODO heart 구현
                # 'heart'    : 1 if Heart.objects.filter(course__id=course.id).filter(user=request.user) else 0 if not request.user else 0
                'places': [
                    {
                        'order_number'   : place.order_number,
                        'place_id'       : place.place.id,
                        'place_name'     : place.place.name,
                        'place_image_url': place.place.image_url,
                        # TODO heart 구현
                        # 'heart'    : 1 if Heart.objects.filter(place__id=place.place.id).filter(user=request.user) else 0 if not request.user else 0
                    }
                    for place in course.courseplace_set.all()
                ]
            }
            return JsonResponse({'message' : 'SUCCESS', "result" : course_detail}, status=200)
        
        except Course.DoesNotExist:
            return JsonResponse({"message" : "COURSE_DOES_NOT_EXIST"}, status=404)
        

###### place<place_id> - 장소 상세 페이지
class PlaceDetailView(View):
    @signin_decorator
    def get(self, request, place_id):
        try:
            place = Place.objects.get(id = place_id)
            result = {
                'id'          : place.id,
                'name'        : place.name,
                'district'    : place.district,
                'latitude'    : place.latitude,
                'longitude'   : place.longitude,
                'work_time'   : place.work_time,
                'price'       : place.price,
                'phone_number': place.phone_number,
                'image_url'   : place.image_url,
                'page_url'    : place.page_url,
                'description' : place.description,
                'category_id' : place.category.id,
                # TODO heart 구현
                # 'heart'    : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0 if not request.user else 0
                'related_course' : [{
                    'id'           : course.course.id,
                    'name'         : course.course.name,
                    'duration_time': course.course.duration_time,
                    'price'        : course.course.price,
                    'image_url'    : course.course.image_url,
                    # TODO heart 구현
                    # 'heart'    : 1 if Heart.objects.filter(course__id=course.course.id).filter(user=request.user) else 0 if not request.user else 0
                } for course in place.courseplace_set.all()]
            }

            return JsonResponse({'message' : 'SUCCESS', "result" :result}, status=200)
        
        except Place.DoesNotExist:
            return JsonResponse({"message" : "PLACE_DOES_NOT_EXIST"}, status=400)



####### nearby - 거리 가까운 장소 목록 페이지
class NearbyPlaceListView(View):
    @signin_decorator
    def get(self, request):
        ws_latitude  = request.GET.get('ws_latitude')
        ws_longitude = request.GET.get('ws_longitude')
        ne_latitude  = request.GET.get('ne_latitude')
        ne_longitude = request.GET.get('ne_longitude')
        

        q = Q()

        q &= Q(latitude__gte=ws_latitude)
        q &= Q(latitude__lte=ne_latitude)
        q &= Q(longitude__gte=ws_longitude)
        q &= Q(longitude__lte=ne_longitude)

        places = Place.objects.filter(q).distinct()
        
        result = [
            {
                'id'       : place.id,
                'name'     : place.name,
                'image_url': place.image_url,
                'latitude' : place.latitude,
                'longitude': place.longitude,
                # TODO 추가구현
                # 'heart'    : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0 if not request.user else 0
            }for place in places
        ]

        return JsonResponse(
            {
                'message'     : 'SUCCESS',
                'result'      : result,
                'total_places': places.count()
            }, status=200)



####### top-places - TOP 20 장소 목록 페이지
class top20ListView(View):
    @signin_decorator
    def get(self,request):
        pass

###### recommend-places - 찜기반 추천 장소 목록 페이지
class RecommendPlaceListView(View):
    @signin_decorator
    def get(self,request):
        pass