from django.urls import path
from django.views.decorators.cache import cache_page

from .views import (
    StudentRegistrationView,
    StudentEnrollCourseView,
    StudentCourseListView,
    StudentCourseDetailView,
)


urlpatterns = [
    path('register/', StudentRegistrationView.as_view(), name='student_registration'),
    path('enroll-course/', StudentEnrollCourseView.as_view(), name='student_enroll_course'),
    path('courses/', StudentCourseListView.as_view(), name='student_course_list'),
    path('course/<pk>/', cache_page(50 * 15)(StudentCourseDetailView.as_view()), name='student_course_detail'),
    path('course/<pk>/<module_id>/', cache_page(50 * 15)(StudentCourseDetailView.as_view()), name='student_course_detail_module'),
]