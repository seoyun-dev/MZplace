import jwt

from django.http        import JsonResponse
from django.conf        import settings

from users.models       import User

def signin_decorator(func):
    def wrapper(self, request, *args, **kwargs):
        user = None
        try:
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
            print(user)
            return func(self, request, *args, **kwargs)
        
        except User.DoesNotExist:
            return JsonResponse({'message': 'USER_DOES_NOT_EXIST'}, status=401)
        
        except ValueError:
            return JsonResponse({'message': 'ENTER_NUMBERS_ONLY'}, status=401)
        
        except jwt.ExpiredSignatureError:
            return JsonResponse({'message': 'EXPIRED_TOKEN'}, status=401)
        
        except jwt.exceptions.DecodeError:
            return JsonResponse({'message': 'INVALID_TOKEN'}, status=401)
        
        except Exception as e:
            return JsonResponse({'message': f'UNKNOWN_ERROR: {e}'}, status=400)

    return wrapper