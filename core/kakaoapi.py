import requests

class KakaoAPI:
    def __init__(self, client_id, redirect_uri):
        self.token_api        = "https://kauth.kakao.com/oauth/token"
        self.user_info_api    = "https://kapi.kakao.com/v2/user/me"
        self.expire_token_api = "https://kapi.kakao.com/v1/user/logout"
        self.redirect_uri     = redirect_uri
        self.client_id        = client_id

    def get_kakao_access_token(self, code):
        body = {
            'grant_type'  : 'authorization_code',
            'client_id'   : self.client_id,
            'redirect_uri': self.redirect_uri,
            'code'        : code
            }
        token_info_res = requests.post(self.token_api, data=body).json()
        kakao_token    = token_info_res.get('access_token')

        if not kakao_token:
            raise Exception('access_token not found')
        
        return kakao_token

    def get_user_kakao_information(self, kakao_token):
        headers = {
            'AUTHORIZATION' : f'Bearer {kakao_token}'
            }
        
        user_kakao_info_res = requests.get(self.user_info_api, headers=headers).json()

        user_kakao_info = {
            'kakao_id'         : user_kakao_info_res['id'],
            'email'            : user_kakao_info_res['kakao_account']['email'],
            'nickname'         : user_kakao_info_res['kakao_account']['profile']['nickname'],
            'profile_image_url': user_kakao_info_res['kakao_account']['profile']['profile_image_url'],
        }

        return user_kakao_info

    def expire_user_access_token(self, kakao_token):
        headers = {
            'AUTHORIZATION' : f'Bearer {kakao_token}'
            }

        expire_token_res = requests.post(self.expire_token_api, headers=headers).json()

        return expire_token_res