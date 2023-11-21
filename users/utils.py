import jwt

from django.http        import JsonResponse
from django.conf        import settings

from users.models       import User

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        user = None
        # kakao-id, naver-id, local-token 로 프론트에서 요청
        kakao_id    = request.META.get('HTTP_KAKAO_ID', None)
        naver_id    = request.META.get('HTTP_NAVER_ID', None)
        local_token = request.META.get('HTTP_LOCAL_TOKEN', None)
        
        if kakao_id:
            kakao_id = int(kakao_id)
            user     = User.objects.get(kakao_id=kakao_id)
        elif naver_id:
            naver_id = int(naver_id)
            user     = User.objects.get(naver_id=naver_id)
        elif local_token:
            payload = jwt.decode(local_token, settings.SECRET_KEY, algorithms=settings.ALGORITHM)
            user    = User.objects.get(id=payload['id'])
        
        request.user = user

        return func(self, request, *args, **kwargs)

    return wrapper