from django.urls import path
from rest_framework import routers
from rest_framework.routers import DefaultRouter

from users.views import UserList, UserRUD, custom_obtain_token





urlpatterns = [
    path('api/v1/users/<id>/', UserRUD.as_view(), name='user-detail'),
    path('api/v1/users/', UserList.as_view(), name='user-list'),
    path('api-token-auth/', custom_obtain_token, name='api-token-auth'),
]
