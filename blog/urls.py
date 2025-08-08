from django.contrib.auth.decorators import login_required
from django.urls import path
from .views import (
    DomainListView,
    CourseListView,
    CourseDetailView,
    CourseCreateView,
    CourseUpdateView,
    CourseDeleteView,
    DomainCourseListView, ProfileListView, SectionDetailView, CourseEnrolledDetailView, InstructorCourseListView,
    UserCourseListView, SectionUpdateView
)
from . import views

urlpatterns = [
    path('', views.landing, name='landing-page'),
    path('domain/', DomainListView.as_view(), name='domain-page'),
    path('profile/',  login_required(ProfileListView.as_view()), name='profile-page'),
    path('search/', views.searchCourses, name='search-course'),
    path('course/', CourseListView.as_view(), name='course-page'),
    path('created_courses/', InstructorCourseListView.as_view(), name='created_courses'),
    path('Mycourses/', UserCourseListView.as_view(), name='Mycourses'),
    path('dashboard/', views.dashData, name='dashboard'),
    path('domain/<str:domainId>/course/', DomainCourseListView.as_view(), name='domain-courses'),
    path('course_detail/<int:pk>/', views.coursdetail, name='course-detail'),
    path('course_enrolled_detail/<int:pk>/', CourseEnrolledDetailView.as_view(), name='course-enrolled-detail'),
    path('section/<int:pk>/', SectionDetailView.as_view(), name='section-detail'),
    path('course/<int:pk>/new-section/', views.createSection, name='section-create'),
    path('section/<int:pk>/update/', SectionUpdateView.as_view(), name='section-update'),
    path('course/new/', views.createCourse, name='course-create'),
    path('course/<int:pk>/update/', CourseUpdateView.as_view(), name='course-update'),
    path('course/<int:pk>/delete/', CourseDeleteView.as_view(), name='course-delete'),
    path('about/', views.about, name='dolphiny-about'),
    path('checkout/<int:pk>/', views.checkout, name="checkout"),
    path('complete/', views.paymentComplete, name="complete"),

]
