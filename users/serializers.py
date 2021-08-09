from django.contrib.auth.models import User
from django.contrib.auth.password_validation import validate_password
from rest_framework import serializers


class ReadOnlyUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ['id', 'username', 'first_name', 'last_name', 'is_active', 'last_login', 'is_superuser']
        read_only_fields = ['last_login', 'is_superuser']
        extra_kwargs = {'is_active': {'required': True}}


class WriteOnlyUserSerializer(serializers.ModelSerializer):
    password = serializers.RegexField(regex=r'^(?=.*[A-Z])(?=.*\d).{8,}$',
                                      required=True, max_length=128, allow_blank=False, allow_null=False)

    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'password', 'is_active']
        extra_kwargs = {'is_active': {'required': True}}