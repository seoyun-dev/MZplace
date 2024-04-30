import json

from django.http  import JsonResponse, QueryDict
from django.views import View

from users.utils import signin_decorator
from places.models import Place, Course
from reviews.models import Review

class ReviewView(View):
    @signin_decorator
    def post(self, request):
        try:
            data    = json.loads(request.body)
            user    = request.user
            content = data['content']
            rating  = data['rating']

            if 'course_id' in data:
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

            elif 'place_id' in data:
                place = Place.objects.get(id=data['place_id'])
                if Review.objects.filter(user=user, place_id=place.id).exists():
                    return JsonResponse({'message': 'REVIEW_ALREADY_EXISTS'}, status=400)
                Review.objects.create(
                    user    = user,
                    place   = place,
                    content = content,
                    rating  = rating
                )
                return JsonResponse({'message':'POST_REVIEW_SUCCESS'}, status=201)

        except Place.DoesNotExist:
            return JsonResponse({"message": "PLACE_NOT_EXIST"}, status=404)
            
        except Course.DoesNotExist:
            return JsonResponse({"message": "COURSE_NOT_EXIST"}, status=404)

        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)


    @signin_decorator
    def put(self, request):
        try:
            data     = json.loads(request.body)
            user     = request.user
            content  = data['content']
            rating   = data['rating']
            
            if 'course_id' in data :
                course_id = data['course_id']
                course    = Course.objects.get(id=course_id)
                review    = Review.objects.get(user=user, course=course)
            elif 'place_id' in data:
                place_id = data['place_id']
                place = Place.objects.get(id=place_id) 
                review = Review.objects.get(user=user, place=place)
            
            review.content = content
            review.rating  = rating
            review.save()
            
            return JsonResponse({'message': 'REVIEW_UPDATED'}, status=200)
        
        except Place.DoesNotExist:
            return JsonResponse({"message": "PLACE_NOT_EXIST"}, status=404)
            
        except Course.DoesNotExist:
            return JsonResponse({"message": "COURSE_NOT_EXIST"}, status=404)

        except Review.DoesNotExist:
            return JsonResponse({'message': 'REVIEW_NOT_FOUND'}, status=404)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

    
    def get(self, request):
        try: 
            type   = request.GET.get('type')
            number = request.GET.get('num')
            if type == 'c':
                course    = Course.objects.get(id=number)
                reviews   = Review.objects.filter(course=course)
            elif type == 'p':
                place    = Place.objects.get(id=number)
                reviews  = Review.objects.filter(place=place)
            else:
                return JsonResponse({'message': 'CHECK_TYPE'}, status=400)
            result = [{
                    'id'        : review.id,
                    'user'      : review.user.nickname,
                    'rating'    : review.rating,
                    'content'   : review.content,
                    'created_at': review.created_at.date(),
                    'updated_at': review.updated_at.date()
                } for review in reviews]

            return JsonResponse({'reviews':result}, status=200)
        
        except KeyError:
            return JsonResponse({'message': 'KEY_ERROR'}, status=400)

        except Place.DoesNotExist:
            return JsonResponse({"message": "PLACE_NOT_EXIST"}, status=404)
            
        except Course.DoesNotExist:
            return JsonResponse({"message": "COURSE_NOT_EXIST"}, status=404)


    @signin_decorator
    def delete(self, request):
        try:
            data = QueryDict(request.body)
            if 'course_id' in data :
                course = Course.objects.get(id=data.get('course_id'))
                Review.objects.get(user=request.user, course=course).delete()
            elif 'place_id' in data:
                place = Place.objects.get(id=data.get('place_id'))
                Review.objects.get(user=request.user, place=place).delete()

            return JsonResponse({"message":"DELETE_SUCCESS"}, status=200)

        except Place.DoesNotExist:
            return JsonResponse({"message": "PLACE_NOT_EXIST"}, status=404)
        
        except Course.DoesNotExist:
            return JsonResponse({"message": "COURSE_NOT_EXIST"}, status=404)

        except Review.DoesNotExist:
            return JsonResponse({"message": "REVIEW_NOT_EXIST"}, status=404)

        except json.JSONDecodeError:
            return JsonResponse({"message":"JSONDecodeError"}, status=400)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)