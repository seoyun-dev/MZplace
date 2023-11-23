from django.urls import path

from .views import HeartView

urlpatterns = [
    path('', HeartView.as_view())
]