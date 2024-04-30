import pandas as pd
import numpy as np
from scipy.stats import mode
from sklearn.metrics import f1_score
from sklearn.metrics import jaccard_score
from sklearn.model_selection import train_test_split

from django.http  import JsonResponse
from django.views import View
from django.db.models import Q
from django.db.models import Count, Avg

from places.models  import Category, Place, FilterPlace, Filter, Course, CoursePlace
from hearts.models  import Heart
from users.utils    import signin_decorator
from reviews.models import Review

import pandas as pd
import numpy as np
from scipy.stats import mode
from sklearn.metrics import jaccard_score
from sklearn.model_selection import train_test_split
from sklearn.metrics.pairwise import cosine_similarity



###### cateogry - 카테고리별 장소 목록 페이지
class CategoryPlaceListView(View):
    @signin_decorator
    def get(self, request, category_id):
        try: 
            category = Category.objects.get(id=category_id)
            page     = int(request.GET.get('page'))
            
            q = Q()
            q &= Q(category__name = category.name)

            if category_id == 6:
                ribbon_num = int(request.GET.get('ribbon'))
                if ribbon_num==0 or ribbon_num==1 or ribbon_num==2 or ribbon_num==3:
                    q &= Q(description__icontains = str(ribbon_num)+'개')
                else:
                    return JsonResponse({'message':'CHECK_RIBBON_NUM'}, status=400)

            else:
                price    = request.GET.get('price')
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
            course         = Course.objects.get(id = course_id)
            reviews        = Review.objects.filter(course_id=course_id)
            review_count   = reviews.count()
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']  # 평균 점수 계산
            course_detail  = {
                'id'            : course.id,
                'name'          : course.name,
                'duration_time' : course.duration_time,
                'price'         : course.price,
                'image_url'     : course.image_url,
                'heart'         : 1 if Heart.objects.filter(course__id=course.id).filter(user=request.user) else 0 if not request.user else 0,
                'reviews_count' : review_count,
                'average_rating': average_rating if average_rating is not None else 0,
                'places'        : [
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
            reviews        = Review.objects.filter(place_id=place_id)
            review_count   = reviews.count()
            average_rating = reviews.aggregate(Avg('rating'))['rating__avg']
            result = {
                'id'            : place.id,
                'name'          : place.name,
                'district'      : place.district,
                'latitude'      : place.latitude,
                'longitude'     : place.longitude,
                'work_time'     : place.work_time,
                'price'         : place.price,
                'phone_number'  : place.phone_number,
                'image_url'     : place.image_url,
                'page_url'      : place.page_url,
                'description'   : place.description,
                'category_id'   : place.category.id,
                'heart'         : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0 if not request.user else 0,
                'reviews_count' : review_count,
                'average_rating': average_rating if average_rating is not None else 0,
                'related_course': [{
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
        
        # 사용자 ID에 해당하는 추천 리스트 가져오기
        recommendations = self.get_recommendations(user.id)
        recommend_id_list = [Place.objects.get(id=place_id) for place_id in recommendations]
        recommendations = [{
                'id'       : place.id,
                'name'     : place.name,
                'image_url': place.image_url,
                'heart'    : 1 if Heart.objects.filter(place__id=place.id).filter(user=request.user) else 0 if not request.user else 0
            }for place in recommend_id_list]

        return JsonResponse({
            'message'        : 'SUCCESS',
            'recommendations': recommendations,
            'total_places'   : len(recommend_id_list)
            }, status=200)


    ### 사용자에게 추천할 장소 id들을 반환하는 메서드
    def get_recommendations(self, user_id):
        # 데이터 전처리
        likes = Heart.objects.values('place_id', 'user_id')
        likes = pd.DataFrame(list(likes))  # Django 쿼리셋을 DataFrame으로 변환
        likes['heart'] = 1
        likes = likes.drop_duplicates(subset=['place_id', 'user_id'], keep='first')

        # for UBCF
        likes_matrix = likes.pivot_table(index='user_id', columns='place_id', values='heart')
        matrix_dummy = likes_matrix.copy().fillna(0)
        user_similarity = self.calculate_jaccard_similarity(matrix_dummy)
        user_similarity = pd.DataFrame(user_similarity, index=likes_matrix.index, columns=likes_matrix.index)

        # for IBCF
        likes_matrix_t = likes_matrix.transpose()
        matrix_dummy_t = likes_matrix_t.copy().fillna(0)
        item_similarity = cosine_similarity(matrix_dummy_t, matrix_dummy_t)
        item_similarity = pd.DataFrame(item_similarity, index=likes_matrix_t.index, columns=likes_matrix_t.index)

        # UBCF + IBCF hybrid - 추천 장소 id 반환
        UBCF_list = self.UBCF_recommender(user_id, 50, likes_matrix, user_similarity)
        IBCF_list = self.IBCF_recommender(user_id, 50, likes_matrix, likes_matrix_t, item_similarity)
        print(len(set(UBCF_list)), len(set(IBCF_list)), len(set(UBCF_list) & set(IBCF_list)))
        intersection = list(set(UBCF_list) & set(IBCF_list))
        
        return intersection


    ### func - UBCF를 위한 자가드 유사도 계산 함수
    def calculate_jaccard_similarity(self, matrix):
        num_users = matrix.shape[0]
        similarities = np.zeros((num_users, num_users))
        for i in range(num_users):
            for j in range(i, num_users):
                similarity = jaccard_score(matrix.iloc[i], matrix.iloc[j])
                similarities[i, j] = similarity
                similarities[j, i] = similarity

        return similarities


    ### UBCF 추천 함수
    def UBCF_recommender(self, user_id, n_items, likes_matrix, user_similarity):
        liked_index = likes_matrix.loc[user_id][likes_matrix.loc[user_id] > 0].index
    
        # 현재 사용자와 유사한 사용자들의 찜한 장소의 평균 예상 찜 여부 계산
        predictions = []
        for place_id in likes_matrix.columns:
            if place_id not in liked_index:
                prediction = self.CF_UBCF(user_id, place_id, likes_matrix, user_similarity)
                # 0이 아닌 것은 제외
                if prediction > 0.4:
                    predictions.append((place_id, prediction))
        
        # 예상 찜 여부를 기준으로 내림차순 정렬 -> 내림차순 장소 id 반환
        predictions.sort(key=lambda x: x[1], reverse=True)
        recommended_items = [place_id for place_id, _ in predictions[:n_items]]
        
        return recommended_items


    ### UBCF 알고리즘 함수
    def CF_UBCF(self, user_id, place_id, likes_matrix, user_similarity):
        if place_id in likes_matrix:
            sim_scores     = user_similarity[user_id].copy()
            place_likes    = likes_matrix[place_id].copy()
            none_likes_idx = place_likes[place_likes.isnull()].index
            place_likes    = place_likes.drop(none_likes_idx)
            sim_scores     = sim_scores.drop(none_likes_idx)

            if sim_scores.sum() != 0.0:
                predicted_likes = np.dot(sim_scores, place_likes) / sim_scores.sum()
            else:
                predicted_likes = 0.0
                
        else:
            predicted_likes = 0.0 # 특정 장소에 대한 좋아요 없는 경우 예측 불가
        return predicted_likes


    ### IBCF 추천 함수
    def IBCF_recommender(self, user_id, n_items, likes_matrix, likes_matrix_t, item_similarity):
        liked_index = likes_matrix.loc[user_id][likes_matrix.loc[user_id] > 0].index
        
        # 모든 장소에 대한 예상 찜 여부 계산
        predictions = []
        for place_id in likes_matrix.columns:
            if place_id not in liked_index:
                prediction = self.CF_IBCF(user_id, place_id, item_similarity, likes_matrix_t)
                # 0이 아닌 것은 제외
                if prediction > 0.4:
                    predictions.append((place_id, prediction))
        
        # 예상 찜 여부를 기준으로 내림차순 정렬
        predictions.sort(key=lambda x: x[1], reverse=True)
        # 상위 n_items개의 장소를 추천
        recommended_items = [place_id for place_id, _ in predictions[:n_items]]
        return recommended_items
    

    ### IBCF 알고리즘 함수
    def CF_IBCF(self, user_id, place_id, item_similarity, likes_matrix_t):
        if place_id in item_similarity:      # 현재 영화가 train set에 있는지 확인
            # 현재 장소와 다른 장소의 similarity 값 가져오기
            sim_scores = item_similarity[place_id]
            # 현 사용자의 모든 찜 값 가져오기
            user_likes = likes_matrix_t[user_id]            
            
            # 사용자가 평가하지 않은 장소 제거
            none_likes_idx = user_likes[user_likes.isnull()].index
            user_likes = user_likes.dropna()
            # 사용자가 평가하지 않은 장소의 similarity 값 제거
            sim_scores = sim_scores.drop(none_likes_idx)
            
            # 현 장소에 대한 예상 찜 계산, 가중치는 현 장소와 사용자가 평가한 장소의 유사도
            if sim_scores.sum() != 0.0:
                predicted_likes = np.dot(sim_scores, user_likes) / sim_scores.sum()
            else:
                predicted_likes = 0.0
        else:
            predicted_likes = 0.0
        return predicted_likes






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