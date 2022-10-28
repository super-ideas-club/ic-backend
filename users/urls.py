from django.urls import path
from . import views

urlpatterns = [
    path('user/register', views.sign_up, name='sign_up'),
    path('user/auth', views.sign_in, name='sign_in'),
]
"""
example: 
urlpatterns = [
    path('api/auth/signup/', views.sign_up, name='sign_up'),
    path('api/auth/signin/', views.sign_in, name='sign_in'),
    path('api/auth/logout/', views.log_out, name='logout'),
    path('api/changeavatar/', views.changeAvatar, name='changeAvatar'),
    # path('api/accounts/data/', views.accountData, name='accountData'),
]
"""