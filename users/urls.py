from django.urls import path
from . import views

urlpatterns = [
    path('api/auth/signup/', views.sign_up, name='sign_up'),
    path('api/auth/signin/', views.sign_in, name='sign_in'),
    path('user/info/', views.get_data, name='get_data'),
    path('api/user/test/', views.test_view, name='test_view'),
]