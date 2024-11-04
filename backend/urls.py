
from unicodedata import name
from django.contrib import admin
from django.urls import path,include
from rest_framework_simplejwt.views import TokenRefreshView, TokenBlacklistView

urlpatterns = [
    path('admin/', admin.site.urls),
    path('',include('lms.urls')),
    path('',include('assignment.urls')),
    path('token/refresh/', TokenRefreshView.as_view(), name='token_refresh'),
    path('token/blacklist/', TokenBlacklistView.as_view(), name='token_blacklist'),
    path('api-auth/', include('rest_framework.urls', namespace='rest_framework'))
]
