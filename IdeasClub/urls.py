from django.urls import path, include
from django.contrib import admin

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('users.urls')),
    path('api/', include('ideasLogic.urls')),
    path('api/messages_system/', include('messages_system.messages_api')),
]
