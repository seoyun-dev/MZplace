import json

from django.http        import JsonResponse
from users.models       import User

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            kakao_id     = request.headers.get('Authorization', None)
            user         = User.objects.get(kakao_id=kakao_id)
            request.user = user
        
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper