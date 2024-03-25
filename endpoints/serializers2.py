import random

from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import serializers

from .models import Categories, SubCategories, SubSubCategories
from .utlis.cache import RedisCache
from .utlis.send_sms import SMSClient

User = get_user_model()  # get the current User model being utilized


class AdminSignupSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True)

    class Meta:
        model = User
        fields = ['username', 'password', 'phone_number']

    def create(self, validated_data):
        user = User.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
            phone_number=validated_data['phone_number']
        )

        admin_group = Group.objects.get(name='Admin')
        user.groups.add(admin_group)

        user.save()
        return user

    # TODO: can add input validation methods here
    def validate_username(self, value):
        if User.objects.filter(username=value).exists():
            raise Exception("Username already exists")
        return value

    def validate_phone_number(self, value):
        """
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must only consist digits")
        """
        if len(value) > 15:
            raise Exception("Phone number is invalid")
        return value


class AdminSigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        try:
            username = data.get('username')
            password = data.get('password')

            if username and password:
                user = get_object_or_404(User, username=username)
                if user.check_password(password):
                    if user.groups.filter(name='Admin').exists():
                        data['user'] = user
                        return data
                    else:
                        raise Exception("User is not Admin")
                else:
                    raise Exception("Passwords do not match")

            else:
                raise serializers.ValidationError("Username and Password is required")
        except Exception as e:
            print("Error while Admin sign-in: ", e)
            raise Exception(e)


class OTPGeneratorSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    reason = serializers.CharField(max_length=255)

    def validate(self, data):
        try:
            username = data.get('username')
            reason = data.get('reason')

            user = get_object_or_404(User, username=username)

            if username and reason:
                generated_otp = random.randint(100000, 999999)
                user_phone_number = user.phone_number

                RedisCache.set_instance(username=username, otp=generated_otp)
                SMSClient.send_otp_sms(phone_number=user_phone_number, reason=reason, otp=generated_otp)

                data['phone_number'] = user_phone_number
                data['username'] = username
                data['otp'] = generated_otp
                return data
            else:
                raise serializers.ValidationError("'Username' and 'Reason' are required")
        except Exception as e:
            print("Error occurred while generating OTP: ", e)
            raise Exception(e)


class OTPVerifierSerializer(serializers.Serializer):
    username = serializers.CharField(max_length=255)
    otp = serializers.CharField(max_length=6)

    def validate(self, data):
        try:
            username = data.get('username')
            otp = data.get('otp')

            if username and otp:
                stored_otp = RedisCache.get_instance(username=username)

                if not stored_otp or stored_otp != otp:
                    data['status'] = 'FAILURE'
                    raise Exception("OTP Expired or is Invalid")

                data['status'] = 'SUCCESS'
                return data
            else:
                raise serializers.ValidationError("'Username' and 'OTP' are required")
        except Exception as e:
            print("Error occurred while verifying OTP: ", e)
            raise Exception(e)


class AdminResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        try:
            username = data.get('username')
            new_password = data.get('new_password')

            if username and new_password:
                user = get_object_or_404(User, username=username)

                user.set_password(new_password)
                user.save()

                data['user'] = user
                return data
            else:
                raise serializers.ValidationError("'Username', 'New Password' are required")
        except Exception as e:
            print("Error occurred while resetting admin password OTP: ", e)
            raise Exception(e)


class SubSubCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = SubSubCategories
        fields = ['name', 'description', 'image', 'document', 'subcategory']


class SubCategorySerializer(serializers.ModelSerializer):
    subsubcategories = SubSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = SubCategories
        fields = ['name', 'description', 'image', 'category', 'subsubcategories']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Categories
        fields = ['name', 'description', 'image', 'subcategories']
