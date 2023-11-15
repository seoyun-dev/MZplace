from django.urls import path

from .views import CategoryPlaceListView, FilterPlaceListView, CourseDetailView, PlaceDetailView
urlpatterns = [
    # 카테고리별 장소 목록 페이지
    path('/category<int:category_id>', CategoryPlaceListView.as_view()),
    # 맞춤 필터 장소 목록 페이지
    path('/filtering', FilterPlaceListView.as_view()),
    # course<course_id> - 코스 상세 페이지
    path('/course<int:course_id>', CourseDetailView.as_view()),
    # place<place_id> - 장소 상세 페이지
    path('/place<int:place_id>', PlaceDetailView.as_view()),
    # top-places - TOP 20 장소 목록 페이지

    # recommend-places - 찜기반 추천 장소 목록 페이지

    # distance-places - 거리별 추천 장소 목록 페이지
]