import jwt

from django.http        import JsonResponse
from django.conf        import settings

from users.models       import User

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        try:
            kakao_id    = request.headers.get('kakao_Authorization', None)
            naver_id    = request.headers.get('naver_Authorization', None)
            local_token = request.headers.get('local_Authorization', None)
            
            if kakao_id:
                user = User.objects.get(kakao_id=kakao_id)
            elif naver_id:
                user = User.objects.get(naver_id=naver_id)
            elif local_token:
                payload = jwt.decode(local_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
                user    = User.objects.get(id=payload['id'])
                user    = User.objects.get(kakao_id=kakao_id)
            
            request.user = user
        
        except User.DoesNotExist:
            return JsonResponse({'message':'INVALID_USER'}, status=400)

        return func(self, request, *args, **kwargs)

    return wrapper