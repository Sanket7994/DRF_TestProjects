from django.urls import path, include
from .views import ListViewAPI, MyTokenObtainPairView
from .views import StudentListView, SchoolListView
from rest_framework_simplejwt.views import TokenRefreshView
from .views import APILogoutView, LoginView, SignupView, PingView


urlpatterns = [
    path('ping', PingView.as_view()),
    path('auth-login', LoginView.as_view()),
    path('auth-signup', SignupView.as_view()),
    path('school/', SchoolListView.as_view()),
    path('student/', StudentListView.as_view()),
    
    path('api/', ListViewAPI.as_view(), name='routes'),
    path('api/token/', MyTokenObtainPairView.as_view(), name='token_obtain_pair'),
    path('api/token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('api/logout_token/', APILogoutView.as_view(), name='logout_token'), 
]