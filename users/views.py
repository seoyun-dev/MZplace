import json
import re

# import bcrypt
# import jwt
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View
from django.conf            import settings

from users.models     import User

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            nickname = data['nickname']
            user_id  = data['user_id']
            password = data['password']


            if User.objects.filter(user_id=user_id).exists():
                return JsonResponse({"message" : "THIS_USER_ID_ALREADY_EXISTS"}, status=400)
            
            # hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')

            User.objects.create(
                nickname = nickname,
                user_id  = user_id,
                password = password
            )

            return JsonResponse({"message" : "SIGNUP_SUCCESS"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"message" : "JSONDecodeError"}, status=404)
    
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)

        except ValidationError as error:
            return JsonResponse({"message" : error.message}, status=400)



class KakaoSocialLoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user, created = User.objects.get_or_create(
                kakao_id   = data['kakao_id'],
                nickname   = data['nickname']
            )

            if created:
                return JsonResponse({"message" : "SIGNUP_SUCCESS"}, status=201)
            
            return JsonResponse({"message" : "LOGIN_SUCCESS"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message" : "JSONDecodeError"}, status=404)
    
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)



class NaverSocialLoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user, created = User.objects.get_or_create(
                naver_id   = data['naver_id'],
                nickname   = data['nickname']
            )

            if created:
                return JsonResponse({"message" : "SIGNUP_SUCCESS"}, status=201)
            
            return JsonResponse({"message" : "LOGIN_SUCCESS"}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message" : "JSONDecodeError"}, status=404)
    
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)



class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(user_id=data['user_id'])

            # if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
            #     return JsonResponse({'message':'INVALID_USER'}, status=401)

            # access_token = jwt.encode({'id': user.id}, settings.SECRET_KEY, settings.ALGORITHM)

            # return JsonResponse({'message':'SUCCESS', 'ACCESS_TOKEN':access_token}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=404)
        except User.DoesNotExist:
            return JsonResponse({'message':'USER_DOES_NOT_EXIST'}, status=404)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)
