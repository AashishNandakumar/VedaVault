import random
from django.contrib.auth import get_user_model
from django.contrib.auth.models import Group
from django.shortcuts import get_object_or_404
from rest_framework import serializers
from django.conf import settings
from urllib.parse import urlparse
import redis
from .models import Categories, SubCategories, SubSubCategories

User = get_user_model()  # get the current User model being utilized

redis_url = urlparse(settings.CACHES['default']['LOCATION'])
redis_host = redis_url.hostname
redis_port = redis_url.port
redis_instance = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)


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
            raise serializers.ValidationError("Username already exists")
        return value

    def validate_phone_number(self, value):
        """
        if not value.isdigit():
            raise serializers.ValidationError("Phone number must only consist digits")
        """
        if len(value) > 15:
            raise serializers.ValidationError("Phone number is invalid")
        return value


class AdminSigninSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        if username and password:
            try:
                user = get_object_or_404(User, username=username)
                if user.check_password(password):
                    if user.groups.filter(name='Admin').exists():
                        data['user'] = user
                        return data
                    else:
                        raise serializers.ValidationError("User is not Admin")
                else:
                    raise serializers.ValidationError("Passwords do not match")
            except Exception as e:
                raise serializers.ValidationError("Invalid credentials")
        else:
            raise serializers.ValidationError("Username and Password is required")


class AdminForgotPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()

    def validate(self, data):
        username = data.get('username')

        if username:
            try:
                user = get_object_or_404(User, username=username)

                if user.groups.filter(name='Admin').exists():
                    phone_number = user.phone_number
                    otp = random.randint(100000, 999999)

                    redis_instance.set(username, otp, ex=500)  # otp expiry = 500 secs (for testing only)
                    print(f"OTP for {phone_number}: {otp}")

                    # TODO: Send the OTP to the client
                    data['otp'] = otp
                    return data
                else:
                    raise serializers.ValidationError("User is not Admin")
            except Exception:
                raise serializers.ValidationError("Username does not exists")
        else:
            raise serializers.ValidationError("Username is required!")


class AdminResetPasswordSerializer(serializers.Serializer):
    username = serializers.CharField()
    otp = serializers.CharField()
    new_password = serializers.CharField()

    def validate(self, data):
        username = data.get('username')
        otp = data.get('otp')
        new_password = data.get('new_password')

        if username and otp and new_password:
            try:
                user = get_object_or_404(User, username=username)
                stored_otp = redis_instance.get(username)
                print(stored_otp, otp)
                if not stored_otp or stored_otp != otp:
                    raise serializers.ValidationError("Invalid or Expired OTP")

                print("ok lmo")

                user.set_password(new_password)
                user.save()
                data['user'] = user
                return data
            except Exception:
                raise serializers.ValidationError("Error in verifying OTP")

        else:
            raise serializers.ValidationError("'Username', 'OTP', 'New Password' are required")


class SubSubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = SubSubCategories
        fields = ['name', 'description', 'image', 'document']


class SubCategorySerializer(serializers.ModelSerializer):
    subsubcategories = SubSubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = SubCategories
        fields = ['name', 'description', 'image', 'subsubcategories']


class CategorySerializer(serializers.ModelSerializer):
    subcategories = SubCategorySerializer(many=True, read_only=True)

    class Meta:
        model = Categories
        fields = ['name', 'description', 'image', 'subcategories']
