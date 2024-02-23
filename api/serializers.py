from rest_framework import serializers
from userregapp.models import UserRegisterModel
from django.contrib.auth.models import User


class RegisterSerializer(serializers.ModelSerializer):
    # created_at = serializers.DateTimeField(format='%Y-%m-%d')
    # edited_at = serializers.DateTimeField(format='%Y-%m-%d')
    class Meta:
        model = UserRegisterModel
        fields = '__all__'
        # exclude = ['created_at', 'edited_at']
        # fields = ['Fullname', 'Email', 'PhoneNumber', 'Skill', 'Location', 'NIN', 'Password', 'ConfirmPassword']
        # depth = 1
        


class LoginSerializer(serializers.Serializer):
    email = serializers.EmailField()
    password = serializers.CharField()



# class UserSerializer(serializers.ModelSerializer):
#     class Meta:
#         model = User
#         fields = ("username", "first_name", "email", "last_name")

