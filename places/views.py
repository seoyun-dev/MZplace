import pandas as pd
import numpy as np
from scipy.stats import mode
from sklearn.metrics import f1_score
from sklearn.metrics import jaccard_score
from sklearn.model_selection import train_test_split

from django.http  import JsonResponse
from django.views import View
from django.db.models import Q
from django.db.models import Count

from places.models import Category, Place, FilterPlace, Filter, Course, CoursePlace
from hearts.models import Heart
from users.utils   import signin_decorator

import pandas as pd
import numpy as np
from scipy.stats import mode
from sklearn.metrics import jaccard_score
from sklearn.model_selection import train_test_split



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
                    'heart'    : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0 if not request.user else 0
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
                'heart'        : 1 if Heart.objects.filter(course__id=course.id).filter(user=request.user) else 0 if not request.user else 0
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

        places      = Place.objects.filter(q).distinct()
        places_list = places[12*(page-1):12*page]

        result = [
            {
                'id'       : place.id,
                'name'     : place.name,
                'image_url': place.image_url,
                'heart'    : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0 if not request.user else 0
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
                'heart'        : 1 if Heart.objects.filter(course__id=course.id).filter(user=request.user) else 0 if not request.user else 0,
                'places'       : [
                    {
                        'order_number'   : place.order_number,
                        'place_id'       : place.place.id,
                        'place_name'     : place.place.name,
                        'place_image_url': place.place.image_url,
                        'place_latitude' : place.place.latitude,
                        'place_longitude': place.place.longitude,
                        'heart'          : 1 if Heart.objects.filter(place__id=place.place.id).filter(user=request.user) else 0 if not request.user else 0
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
                'heart'    : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0 if not request.user else 0,
                'related_course' : [{
                    'id'           : course.course.id,
                    'name'         : course.course.name,
                    'duration_time': course.course.duration_time,
                    'price'        : course.course.price,
                    'image_url'    : course.course.image_url,
                    'heart'        : 1 if Heart.objects.filter(course__id=course.course.id).filter(user=request.user) else 0 if not request.user else 0
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
                'heart'    : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0 if not request.user else 0
            }for place in places
        ]

        return JsonResponse(
            {
                'message'     : 'SUCCESS',
                'result'      : result,
                'total_places': places.count()
            }, status=200)



####### TOP 20 장소 목록 페이지
class Top20ListView(View):
    @signin_decorator
    def get(self,request):
        top_20_places_courses = (
            Heart.objects.values('place', 'course')
            .annotate(total_hearts=Count('id'))
            .distinct()
            .order_by('-total_hearts')[:20]
        )

        result = [
            {
                'type'     : 'place',
                'id'       : Place.objects.get(id=place_or_course['place']).id,
                'name'     : Place.objects.get(id=place_or_course['place']).name,
                'image_url': Place.objects.get(id=place_or_course['place']).image_url,
                'heart'          : 1 if Heart.objects.filter(place__id=Place.objects.get(id=place_or_course['place']) .id).filter(user=request.user) else 0 if not request.user else 0
            } 
            if place_or_course['place']
            else {
                'type'     : 'course',
                'id'       : Course.objects.get(id=place_or_course['course']).id,
                'name'     : Course.objects.get(id=place_or_course['course']).name,
                'image_url': Course.objects.get(id=place_or_course['course']).image_url,
                'heart'           : 1 if Heart.objects.filter(place__id=Course.objects.get(id=place_or_course['course']).id).filter(user=request.user) else 0 if not request.user else 0
            }
            for place_or_course in top_20_places_courses
        ]

        return JsonResponse(
            {
                'message'     : 'SUCCESS',
                'result'      : result,
            }, status=200)



###### 찜 기반 추천 장소 목록 페이지
class RecommendPlaceListView(View):
    @signin_decorator
    def get(self, request):
        user = request.user
        page = int(request.GET.get('page'))

        # UBCF 알고리즘 수행
        recommend_id_list = self.recommend_places(user.id, 20).to_dict()
        recommend_place_list = [Place.objects.get(id=place_id) for place_id in recommend_id_list]
        recommendations = [{
                'id'       : recommend_place.id,
                'name'     : recommend_place.name,
                'image_url': recommend_place.image_url,
                'heart'    : 1 if Heart.objects.filter(place__id=recommend_place.id).filter(user=request.user) else 0 if not request.user else 0
            }for recommend_place in recommend_place_list[12*(page-1):12*page]]

        # IBCF 알고리즘 수행
        # ibcf_recommendations = calculate_ibcf_recommendations(user)

        # UBCF와 IBCF의 추천 결과를 결합하여 하이브리드 추천 생성
        # hybrid_recommendations = combine_recommendations(ubcf_recommendations, ibcf_recommendations).distinct()
        # result = [
        #     {
        #         'id'       : recommendation['place_id'],
        #         'name'     : place.name,
        #         'image_url': place.image_url,
        #         'heart'    : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0 if not request.user else 0
        #     } for recommendation in ubcf_recommendations
        # ]
        return JsonResponse({
            'message'        : 'SUCCESS',
            'recommendations': recommendations,
            }, status=200)



    #### UBCF
    def recommend_places(self, user_id, n_items):
        likes = Heart.objects.values('place_id', 'user_id')
        likes = pd.DataFrame(list(likes))  # Django 쿼리셋을 DataFrame으로 변환

        likes['heart'] = 1
        likes = likes.drop_duplicates(subset=['place_id', 'user_id'], keep='first')

        x = likes.copy()
        y = likes['user_id']

        # train, test 분리
        x_train, x_test, y_train, y_test = train_test_split(x, y, test_size=0.25, stratify=y)

        # 전체 데이터로 full matrix와 자가드 유사도 구하기 
        likes_matrix = likes.pivot_table(index='user_id', columns='place_id', values='heart')
        matrix_dummy = likes_matrix.copy().fillna(0)
        user_similarity = self.calculate_jaccard_similarity(matrix_dummy)
        user_similarity = pd.DataFrame(user_similarity, index=likes_matrix.index, columns=likes_matrix.index)

        return self.recommender(user_id, n_items, likes_matrix, user_similarity)
    
    ### 자가드 유사도 계산 함수
    def calculate_jaccard_similarity(self, matrix):
        num_users = matrix.shape[0]
        similarities = np.zeros((num_users, num_users))

        for i in range(num_users):
            for j in range(i, num_users):
                similarity = jaccard_score(matrix.iloc[i], matrix.iloc[j])
                similarities[i, j] = similarity
                similarities[j, i] = similarity

        return similarities

    def recommender(self, user_id, n_items, likes_matrix, user_similarity):
        predictions = []
        liked_index = likes_matrix.loc[user_id][likes_matrix.loc[user_id] > 0].index    # 이미 찜하기 누른 장소 인덱스 가져옴
        #print("liked_index", liked_index)
        items = likes_matrix.loc[user_id].drop(liked_index) # 찜하기 누른 장소 제외하고 추천하기 위해
        #print(items)
    
        for item in items.index:
            predictions.append(self.cf_binary(user_id, item, likes_matrix, user_similarity))                   # 예상 1, 0계산
        recommendations = pd.Series(data=predictions, index=items.index, dtype=float)
        recommendations = recommendations.sort_values(ascending=False)
        recommendations = recommendations[recommendations==1.0]
        return recommendations
    

    def cf_binary(self, user_id, place_id, likes_matrix, user_similarity):
        # 해당 함수의 내용을 이곳에 추가
        if place_id in likes_matrix:
            sim_scores     = user_similarity[user_id].copy()
            place_likes    = likes_matrix[place_id].copy()
            none_likes_idx = place_likes[place_likes.isnull()].index
            place_likes    = place_likes.drop(none_likes_idx)
            sim_scores     = sim_scores.drop(none_likes_idx)

            if sim_scores.sum() != 0.0:
                predicted_likes = np.dot(sim_scores, place_likes) / sim_scores.sum()
            else:
                predicted_likes = mode(place_likes, keepdims=True).mode[0]
                #predicted_likes = 0.0

        else:
            predicted_likes = 0.0 # 특정 장소에 대한 좋아요 없는 경우 예측 불가

        return predicted_likes
    

    
    
    #### IBCF
    def calculate_ibcf_recommendations(user):
        # IBCF 알고리즘 수행하여 사용자에게 추천할 장소 or 코스 추출
        pass


    def combine_recommendations(label_recommendations, ubcf_recommendations, ibcf_recommendations):
        # UBCF와 IBCF의 추천 결과를 결합하여 하이브리드 추천 생성하는 방법 구현
        pass





# ###### 하트 확인용
class Top100ListView(View):
    @signin_decorator
    def get(self,request):
        top_20_places_courses = (
            Heart.objects.values('place', 'course')
            .annotate(total_hearts=Count('id'))
            .distinct()
            .order_by('-total_hearts')[:500]
        )

        result = [
            {
                'type'       : 'place',
                'id'         : Place.objects.get(id=place_or_course['place']).id,
                'name'       : Place.objects.get(id=place_or_course['place']).name,
                'image_url'  : Place.objects.get(id=place_or_course['place']).image_url,
                'total_heart': len(Heart.objects.filter(place__id=Place.objects.get(id=place_or_course['place']).id).distinct()) 
            } 
            if place_or_course['place']
            else {
                'type'     : 'course',
                'id'       : Course.objects.get(id=place_or_course['course']).id,
                'name'     : Course.objects.get(id=place_or_course['course']).name,
                'image_url': Course.objects.get(id=place_or_course['course']).image_url,
                'heart'           : 1 if Heart.objects.filter(place__id=Course.objects.get(id=place_or_course['course']).id).filter(user=request.user) else 0 if not request.user else 0
            }
            for place_or_course in top_20_places_courses
        ]

        return JsonResponse(
            {
                'message'     : 'SUCCESS',
                'result'      : result,
                'total_places': top_20_places_courses.count()
            }, status=200)