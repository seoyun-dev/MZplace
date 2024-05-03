import json
import requests

import bcrypt
import jwt
from django.http            import JsonResponse
from django.core.exceptions import ValidationError
from django.views           import View
# from django.conf            import settings

from mz import settings
from users.models           import User
from users.utils            import signin_decorator

class SignUpView(View):
    def post(self, request):
        try:
            data     = json.loads(request.body)
            nickname = data['nickname']
            user_id  = data['user_id']
            password = data['password']

            if User.objects.filter(user_id=user_id).exists():
                return JsonResponse({"message" : "THIS_USER_ID_ALREADY_EXISTS"}, status=400)
            
            hashed_password = bcrypt.hashpw(password.encode('UTF-8'), bcrypt.gensalt()).decode('UTF-8')

            User.objects.create(
                nickname = nickname,
                user_id  = user_id,
                password = hashed_password
            )

            return JsonResponse({"message" : "SIGNUP_SUCCESS"}, status=201)

        except json.JSONDecodeError:
            return JsonResponse({"message" : "JSONDecodeError"}, status=400)
    
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)



class KakaoSocialLoginView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)

            user, created = User.objects.get_or_create(
                kakao_id   = data['kakao_id'],
                nickname   = data['nickname']
            )

            if created:
                return JsonResponse({"message" : "SIGNUP_SUCCESS", "nickname" : data['nickname']}, status=201)
            
            return JsonResponse({"message" : "LOGIN_SUCCESS", "nickname" : data['nickname']}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({"message" : "JSONDecodeError"}, status=400)
    
        except KeyError:
            return JsonResponse({"message" : "KEY_ERROR"}, status=400)



class NaverSocialLoginView(View):
    def post(self, request):
        ### 프론트한테 코드 받아 네이버 전달 > 네이버에게서 토큰 받기
        code = request.body.decode('utf-8').strip('"')  # 요청 본문에서 코드 추출

        grant_type    = "authorization_code"
        client_id     = settings.NAVER_CLIENT_ID
        client_secret = settings.NAVER_CLIENT_SECRET
        code          = code

        parameters = f"grant_type={grant_type}&client_id={client_id}&client_secret={client_secret}&code={code}"

        # token request
        token_request = requests.get(
            f"https://nid.naver.com/oauth2.0/token?{parameters}"
        )

        token_response_json = token_request.json()
        error = token_response_json.get("error", None)
        print(token_response_json)
        print(error)

        if error is not None:
            return JsonResponse({"message" : "🙀 토큰 가져오기 실패!!!"}, status=400)
        
        access_token = token_response_json.get("access_token")

        ### 네이버한테서 받은 토큰 다시 네이버한테 전달 > id, user 받기 > 프론트한테 전달
        # 네이버 사용자 정보 요청
        headers = {
            "Authorization": f"Bearer {access_token}",
            "Content-Type": "application/json"
        }

        response = requests.get('https://openapi.naver.com/v1/nid/me', headers=headers)
        user_info = response.json()

        if response.status_code != 200:
            return JsonResponse({'message': 'Failed to get user info from Naver'}, status=400)

        # 네이버 API에서 사용자 정보 추출
        naver_id = user_info.get('response', {}).get('id', None)
        name = user_info.get('response', {}).get('name', None)

        if not naver_id:
            return JsonResponse({'message': 'Naver ID not provided'}, status=400)

        # 사용자 정보를 데이터베이스에 저장하거나 업데이트
        user, created = User.objects.update_or_create(
            naver_id = naver_id,
            nickname = name
        )

        # 응답 데이터 준비
        data = {
            'message': 'User signup' if created else 'User login',
            'name': name,
            'naver_id': naver_id
        }
        return JsonResponse(data, status=200)



class LogInView(View):
    def post(self, request):
        try:
            data = json.loads(request.body)
            user = User.objects.get(user_id=data['user_id'])
            if not bcrypt.checkpw(data['password'].encode('utf-8'), user.password.encode('utf-8')):
                return JsonResponse({'message':'INVALID_USER'}, status=401)

            access_token= jwt.encode({'id': user.id}, settings.SECRET_KEY, settings.ALGORITHM)

            return JsonResponse({'message':'SUCCESS', 'nickname': user.nickname, 'ACCESS_TOKEN':access_token}, status=200)

        except json.JSONDecodeError:
            return JsonResponse({'message':'JSONDecodeError'}, status=400)
        except User.DoesNotExist:
            return JsonResponse({'message':'USER_DOES_NOT_EXIST'}, status=404)
        except KeyError:
            return JsonResponse({'message':'KEY_ERROR'}, status=400)



class DeleteView(View):
    @signin_decorator
    def delete(self, request):
        try:
            if not request.user:
                return JsonResponse({'message':'WRITE_ID_OR_TOKEN'}, status=401)
            if request.user.user_id:
                user = User.objects.get(user_id=request.user.user_id)
            elif request.user.kakao_id:
                user = User.objects.get(kakao_id=request.user.kakao_id)
            elif request.user.naver_id:
                user = User.objects.get(naver_id=request.user.naver_id)

            if request.user == user:  # 현재 로그인한 사용자와 삭제 대상 사용자가 같은 경우
                user.delete()
                return JsonResponse({'message':'USER_DELETED'}, status=200)
            else:
                return JsonResponse({'message':'USER_DOES_NOT_HAVE_PERMISSION'}, status=401)
            

        except User.DoesNotExist:
            return JsonResponse({'message':'USER_DOES_NOT_EXIST'}, status=401)