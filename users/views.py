from django.contrib.auth.models import User
from django.shortcuts import render
from drf_yasg.openapi import Response
from drf_yasg.utils import swagger_auto_schema
from rest_framework import generics, status
from rest_framework.permissions import IsAdminUser
from rest_framework.authtoken.views import ObtainAuthToken, AuthTokenSerializer
from rest_framework.authtoken.models import Token
from rest_framework.response import Response as drf_Response

from users.serializers import ReadOnlyUserSerializer, WriteOnlyUserSerializer


class AuthToken(ObtainAuthToken):
    @swagger_auto_schema(responses={200: '{"token": string}'})
    def post(self, request, *args, **kwargs):
        return super().post(request, *args, **kwargs)


custom_obtain_token = AuthToken.as_view()


class UserList(generics.ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = ReadOnlyUserSerializer

    def get_serializer_class(self):
        if self.request.method == 'POST':
            return WriteOnlyUserSerializer
        return self.serializer_class

    # @swagger_auto_schema(responses={201: "'token': 'string'"})
    def get(self, request, *args, **kwargs):
        return super(UserList, self).get(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_201_CREATED: Response(
                description="",
                schema=ReadOnlyUserSerializer,
            )
        }
    )
    def post(self, request, *args, **kwargs):
        return super(UserList, self).post(request, *args, **kwargs)

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        serializer = ReadOnlyUserSerializer(instance=serializer.instance)
        return drf_Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)

    def perform_create(self, serializer):
        serializer.save()


class UserRUD(generics.RetrieveUpdateDestroyAPIView):
    lookup_url_kwarg = 'id'
    queryset = User.objects.all()
    serializer_class = ReadOnlyUserSerializer

    def get_serializer_class(self):
        if self.request.method in ['PUT', 'PATCH']:
            return WriteOnlyUserSerializer
        return self.serializer_class

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: Response(
                description="",
                schema=ReadOnlyUserSerializer,
            )
        }
    )
    def put(self, request, *args, **kwargs):
        return super(UserRUD, self).put(request, *args, **kwargs)

    @swagger_auto_schema(
        responses={
            status.HTTP_200_OK: Response(
                description="",
                schema=ReadOnlyUserSerializer,
            )
        }
    )
    def patch(self, request, *args, **kwargs):
        return super(UserRUD, self).patch(request, *args, **kwargs)

    def update(self, request, *args, **kwargs):
        partial = kwargs.pop('partial', False)
        instance = self.get_object()
        serializer = WriteOnlyUserSerializer(instance, data=request.data, partial=partial)
        serializer.is_valid(raise_exception=True)
        self.perform_update(serializer)
        serializer = ReadOnlyUserSerializer(instance)

        if getattr(instance, '_prefetched_objects_cache', None):
            # If 'prefetch_related' has been applied to a queryset, we need to
            # forcibly invalidate the prefetch cache on the instance.
            instance._prefetched_objects_cache = {}

        return drf_Response(serializer.data)
