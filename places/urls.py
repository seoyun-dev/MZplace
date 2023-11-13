from django.urls import path

from .views import CategoryPlaceListView
urlpatterns = [
    # 카테고리별 장소 목록 페이지
    path('/category<int:category_id>', CategoryPlaceListView.as_view())
    # filter-places - 맞춤 필터 장소 목록 페이지
    
    # course<course_id> - 코스 상세 페이지

    # place<place_id> - 장소 상세 페이지

    # top-places - TOP 20 장소 목록 페이지

    # recommend-places - 찜기반 추천 장소 목록 페이지

    # distance-places - 거리별 추천 장소 목록 페이지
]