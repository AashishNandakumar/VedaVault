from django.contrib.auth.models import Group, User
from rest_framework import serializers
from . import models

"""
class CustomUserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'email', 'username']

    def create(self, validated_data):
        user = User.objects.create_user(**validated_data)

        user_type = self.context.get('user_type')

        group = Group.objects.get(name=user_type)

        user.groups.add(group)

        return user


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = models.Category
        fields = "__all__"


class SubCategorySerializerOnId(serializers.ModelSerializer):

    category_id = serializers.SerializerMethodField('get_category_id2')

    def get_category_id2(self, obj):
        print("categoryId: ", self.context.get('categoryId'))
        return self.context.get('categoryId')

    class Meta:
        model = models.SubCategory
        fields = ["name", "description", "image_url", "category_id"]


class SubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SubCategory
        fields = "__all__"


class SubSubCategorySerializer(serializers.ModelSerializer):

    class Meta:
        model = models.SubSubCategory
        fields = "__all__"


class SubSubCategorySerializerOnId(serializers.ModelSerializer):

    sub_category_id = serializers.SerializerMethodField('get_sub_sub_category_id')

    def get_sub_sub_category_id(self, obj):
        return self.context.get('subCategoryId')

    class Meta:
        model = models.SubSubCategory
        fields = ["name", "description", "image_url", "sub_category_id"]
"""