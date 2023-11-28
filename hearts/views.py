import json

from django.http   import JsonResponse
from django.views  import View

from users.utils   import signin_decorator
from places.models import Place, Course
from .models       import Heart
from django.http   import QueryDict

class HeartView(View):
    @signin_decorator
    def post(self, request):
        try:
            data  = json.loads(request.body)
            if data['type'] == 'c':
                course = Course.objects.get(id=data['course_id'])
                Heart.objects.create(
                course = course,
                user   = request.user
                )
            elif data['type'] == 'p':
                place = Place.objects.get(id=data['place_id'])
                Heart.objects.create(
                place = place,
                user  = request.user
                )
            return JsonResponse({"message" : "ADD_TO_HEART_SUCCESS"}, status=201)

        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)
        
        except json.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=400)


    @signin_decorator
    def get(self, request):
        hearts = [
            {
                'heart_id' : heart.id,
                'type'     : 'place',
                'id'       : heart.place.id,
                'name'     : heart.place.name,
                'image_url': heart.place.image_url,
                'heart'    : 1 if Heart.objects.filter(place__id=heart.place.id).filter(user=request.user) else 0
                if not request.user else 0} 
                if heart.place
                else {
                    'heart_id' : heart.id,
                    'type'     : 'course',
                    'id'       : heart.course.id,
                    'name'     : heart.course.name,
                    'image_url': heart.course.image_url,
                    'heart'    : 1 if Heart.objects.filter(course__id=heart.course.id).filter(user=request.user) else 0
                    if not request.user else 0}
            for heart in Heart.objects.filter(user=request.user).distinct()]
        return JsonResponse({"message" : "SUCCESS", "hearts" : hearts}, status=200)
    

    @signin_decorator
    def delete(self, request):
        try:
            data = QueryDict(request.body)
            if data['type'] == 'c':
                course = Course.objects.get(id=data.get('course_id'))
                Heart.objects.filter(user=request.user, course=course).delete()

            if data.get('type') == 'p':
                place = Place.objects.get(id=data.get('place_id'))
                Heart.objects.filter(user=request.user, place=place).delete()
            
            return JsonResponse({"message":"DELETE_SUCCESS"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message":"JSONDecodeError"}, status=400)
        
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)