import json

from django.http  import JsonResponse
from django.views import View
from django.db.models import Q, Count, Sum, IntegerField, OuterRef, Subquery

from users.utils import signin_decorator
from places.models import Place, Course
from reviews.models import Review
from enum import Enum

class ReviewView(View):
    @signin_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = data['content']
            rating  = data['rating']

            if data['type'] == 'c':
                course = Course.objects.get(id=data['course_id'])
                if Review.objects.filter(user=user, course_id=course.id).exists():
                    return JsonResponse({'message': 'REVIEW_ALREADY_EXISTS'}, status=400)
                Review.objects.create(
                    user    = user,
                    course  = course,
                    content = content,
                    rating  = rating
                )
                return JsonResponse({'message':'SUCCESS'}, status=201)

            elif data['type'] == 'p':
                place = Place.objects.get(id=data['place_id'])
                if Review.objects.filter(user=user, place_id=place.id).exists():
                    return JsonResponse({'message': 'REVIEW_ALREADY_EXISTS'}, status=400)
                Review.objects.create(
                    user    = user,
                    place   = place,
                    content = content,
                    rating  = rating
                )
                return JsonResponse({'message':'SUCCESS'}, status=201)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)

        except Review.DoesNotExist:
            return JsonResponse({"message": "REVIEW_NOT_EXIST"}, status=404)


    @signin_decorator
    def put(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = data['content']
            rating  = data['rating']
            
            # 기존 리뷰 찾기
            review         = Review.objects.get(user=user, place_id=place_id)
            review.content = content
            review.rating  = rating
            review.save()
            
            return JsonResponse({'message': 'REVIEW_UPDATED'}, status=200)
        
        except Review.DoesNotExist:
            return JsonResponse({'message': 'REVIEW_NOT_FOUND'}, status=404)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    
    def get(self, request, place_id):
        reviews = Review.objects.filter(place_id=place_id)

        result = [{
                'id'        : review.id,
                'user'      : review.user.name,
                'rating'    : review.rating,
                'content'   : review.content,
                'created_at': review.created_at.date()
            } for review in reviews]

        return JsonResponse({'review':result}, status=200)