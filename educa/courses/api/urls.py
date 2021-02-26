from django.urls import path, include
from rest_framework import routers

from .views import (
    SubjectListView,
    SubjectDetailsView,
    # CourseEnrollView,
    CourseViewSet,
)

app_name = 'courses'

router = routers.DefaultRouter()
router.register('courses', CourseViewSet)


urlpatterns = [
    path('subjects/', SubjectListView.as_view(), name='api_subject_list'),
    path('subjects/<int:pk>/', SubjectDetailsView.as_view(), name='api_subject_detail'),
    # path('courses/<int:pk>/enroll/', CourseEnrollView.as_view(), name='api_course_enroll'),
    path('', include(router.urls)),
]
