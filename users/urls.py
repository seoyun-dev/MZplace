from django.urls import path

from .views import SignUpView, LogInView, KakaoSocialLoginView, NaverSocialLoginView, DeleteView

urlpatterns = [
    path('/login', LogInView.as_view()),
    path('/kakaologin', KakaoSocialLoginView.as_view()),
    path('/naverlogin', NaverSocialLoginView.as_view()),
    path('/signup', SignUpView.as_view()),
    path('/delete', DeleteView.as_view())
]