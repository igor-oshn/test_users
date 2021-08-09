"""users_test_app URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf.urls import url
from django.urls import path, include, re_path
from drf_yasg import openapi
from drf_yasg.generators import OpenAPISchemaGenerator
from drf_yasg.views import get_schema_view
from rest_framework import permissions
from rest_framework.authtoken import views

from users.urls import urlpatterns as users_urls

# class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
#     def get_schema(self, *args, **kwargs):
#         schema = super().get_schema(*args, **kwargs)
#         schema.basePath = '/api/v1/' # API prefix
#         return schema

schema_view = get_schema_view(
    openapi.Info(
      title="Users App Test",
      default_version='v1',
      description="Test description",
      license=openapi.License(name="BSD License"),
    ),
    # generator_class=CustomOpenAPISchemaGenerator,
    public=True,
    permission_classes=[permissions.AllowAny],
)



urlpatterns = [
    path('swagger/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger-ui'),
    path('', include(users_urls)),
    # path('api/v1/api-token-auth/', views.obtain_auth_token),
]