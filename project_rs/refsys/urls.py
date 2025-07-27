from django.contrib.auth.views import LogoutView
from django.urls import path, include
from rest_framework.authtoken.views import obtain_auth_token

from . import views

urlpatterns = [
    path('', views.HomePageView.as_view(), name='home'),
    path('authorization/', views.NumberFormPageView.as_view(), name='number_form'),
    path('checkcode/', views.CheckCodeFormPageView.as_view(), name='check_code_form'),
    path('profile/', views.ProfileView.as_view(), name='profile'),
    path('logout/', LogoutView.as_view(), name='logout'),
    path('api/auth/', include('rest_framework.urls')),
    path('api/request_code/', views.APIRequestCode.as_view(), name='api_request_code'),
    path('api/check_code/', views.APICheckCode.as_view(), name='api_check_code'),
    path('api/profile/', views.APIProfileView.as_view(), name='api_profile'),

]
# urlpatterns += [
#     path('api-token-auth/', obtain_auth_token)
# ]