DATABASES = {
    'default' : {
        'ENGINE'  : 'django.db.backends.mysql',
        'NAME'    : 'mz',
        'USER'    : 'root',
        'PASSWORD': '0212',
        'HOST'    : '127.0.0.1',
        'PORT'    : '3306',
    }
}

# ALGORITHM = 'HS256'

SECRET_KEY = 'django-insecure-^-y79v##dj12zczrep5+w)i6ll+=nrcdjx&4=mkwt@@-c5292x'
#settings.py에 있는 secret_key 를 사용합니다.

KAKAO_REST_API_KEY = ''
KAKAO_REDIRECT_URI = 'http://13.125.232.99:8000/users/login'