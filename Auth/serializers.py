from rest_framework import serializers
from .models import User
from django.contrib.auth.hashers import make_password


class UserSerializer(serializers.ModelSerializer):
    confirm_password = serializers.CharField(min_length=6, max_length=15)
    email = serializers.EmailField(required=True)
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email', 'mobile', 'role', 'password', 'confirm_password' ]

    def validate(self, data):
        if User.objects.filter(email=data['email']).exists():
            raise serializers.ValidationError("This email is already registered! Try with different one")
        if data.get('password') != data.get('confirm_password'):
            raise serializers.ValidationError('Password does not match')
        data['password'] = make_password(data['password'])
        return data

    def create(self, validated_data):
        validated_data.pop('confirm_password')
        user = User.objects.create(**validated_data)
        return user

