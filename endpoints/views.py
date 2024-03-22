from urllib.parse import urlparse
from rest_framework.response import Response
from rest_framework.throttling import AnonRateThrottle, UserRateThrottle
from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework import status
from django.shortcuts import get_object_or_404
from django.conf import settings
from django.contrib.auth.models import User, Group
from . import serializers
from . import models
from dotenv import load_dotenv
import boto3
import uuid
import random
import redis
import json
import os

load_dotenv()


# views to handle 'Categories' logic
class CategoryBulk(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        try:
            category_serializer = serializers.CategorySerializer(data=request.data)

            category_serializer.is_valid(raise_exception=True)

            category_serializer.save()

            return Response({"message": "Success in adding 'Category' object"}, status.HTTP_201_CREATED)

        except Exception as e:
            print("Failed to store 'Category' Information: ", e)
            return Response({"error": "Error in adding 'Category' object"}, status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        try:
            all_category_obj = models.Category.objects.all()
            print(all_category_obj)

            all_category_obj_serializer = serializers.CategorySerializer(all_category_obj, many=True)

            return Response(all_category_obj_serializer.data, status.HTTP_200_OK)

        except Exception as e:
            print("Failed to fetch 'Category' Information: ", e)
            return Response({"error": "Error in fetching 'Category' object"}, status.HTTP_400_BAD_REQUEST)


class CategoryParticular(APIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, **kwargs):
        try:
            category_obj = get_object_or_404(models.Category, id=kwargs['categoryId'])

            category_obj.delete()
            return Response({"message": "Successfully deleted 'Category' object"}, status.HTTP_204_NO_CONTENT)
        except Exception as e:
            print("Failed to delete 'Category' information: ", e)
            return Response({"error": "Error in deleting 'Category' object"}, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, **kwargs):
        try:
            category_obj = get_object_or_404(models.Category, id=kwargs['id'])

            category_serializer = serializers.CategorySerializer(category_obj, data=request.data, partial=True)

            category_serializer.is_valid(raise_exception=True)

            category_serializer.save()

            return Response({"message": "Successfully updated 'Category' object"}, status.HTTP_206_PARTIAL_CONTENT)

        except Exception as e:
            print("Failed to update 'Category' information: ", e)
            return Response({"error": "Error in updating 'Category' object"}, status.HTTP_400_BAD_REQUEST)


# views to handle 'SubCategories' logic
class SubCategoryBulk(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):

        try:
            sub_category_objs = models.SubCategory.objects.filter(category_id=kwargs['categoryId'])
            print(sub_category_objs)

            serialized_sub_category_objs = serializers.SubCategorySerializer(sub_category_objs, many=True)

            return Response(serialized_sub_category_objs.data, status.HTTP_200_OK)

        except Exception as e:
            print("Failed to fetch 'SubCategory' information: ", e)
            return Response({"error": "Error in fetching 'SubCategory' object"}, status.HTTP_400_BAD_REQUEST)

    def post(self, request, **kwargs):

        try:
            serializer = serializers.SubCategorySerializerOnId(data=request.data, context={'categoryId': kwargs['categoryId']})  # optimize: can just append the 'context' to request, so we can use only one serializer

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response({"message": "Successfully added 'SubCategory' object" + json.dumps(serializer.data)}, status.HTTP_201_CREATED)

        except Exception as e:
            print("Failed to add 'SubCategory' information: ", e)
            return Response({"error": "Error in adding 'SubCategory' object"}, status.HTTP_400_BAD_REQUEST)


class SubCategoryParticular(APIView):

    permission_classes = [IsAuthenticated]

    def delete(self, request, **kwargs):

        try:
            sub_category_obj = get_object_or_404(models.SubCategory, id=kwargs['subCategoryId'], category_id=kwargs['categoryId'])

            sub_category_obj.delete()

            return Response({"message": "Successfully deleted 'SubCategory' object"}, status.HTTP_204_NO_CONTENT)

        except Exception as e:
            print("Failed to delete 'SubCategory' information: ", e)
            return Response({"error": "Error in deleting 'SubCategory' object"}, status.HTTP_400_BAD_REQUEST)

    def patch(self, request, **kwargs):

        try:
            sub_category_obj = get_object_or_404(models.SubCategory, id=kwargs['subCategoryId'], category_id=kwargs['categoryId'])
            print(sub_category_obj)
            serializer = serializers.SubCategorySerializer(instance=sub_category_obj, data=request.data, partial=True)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response({"message": "Successfully updated 'SubCategory' object"}, status.HTTP_206_PARTIAL_CONTENT)

        except Exception as e:
            print("Failed to update 'SubCategory' information: ", e)
            return Response({"error": "Error in updating 'SubCategory' object"}, status.HTTP_400_BAD_REQUEST)


# views to handle SubSubCategory logic
class SubSubCategoryBulk(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, **kwargs):

        try:
            sub_sub_category_obj = models.SubSubCategory.objects.filter(sub_category_id=kwargs['subCategoryId'])

            serializer = serializers.SubSubCategorySerializer(instance=sub_sub_category_obj, many=True)

            return Response(serializer.data, status.HTTP_200_OK)

        except Exception as e:
            print("Failed to fetch 'SubSubCategory' information: ", e)
            return Response({"error": "Error in fetching 'SubSubCategory' object"}, status.HTTP_400_BAD_REQUEST)

    def post(self, request, **kwargs):

        try:
            serializer = serializers.SubSubCategorySerializerOnId(data=request.data, context={'subCategoryId': kwargs['subCategoryId']})

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response({"message": "Successfully added 'SubSubCategory' object" + json.dumps(serializer.data)}, status.HTTP_201_CREATED)

        except Exception as e:
            print("Failed to add 'SubSubCategory' information: ", e)
            return Response({"error": "Error in adding 'SubSubCategory' object"}, status.HTTP_400_BAD_REQUEST)


class SubSubCategoryParticular(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request, **kwargs):
        try:
            sub_sub_category_obj = get_object_or_404(models.SubSubCategory, id=kwargs['subSubCategoryId'], sub_category_id=kwargs['subCategoryId'])

            serializer = serializers.SubSubCategorySerializer(instance=sub_sub_category_obj, data=request.data, partial=True)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response({"message": "Successfully updated 'SubSubCategory' object"}, status.HTTP_206_PARTIAL_CONTENT)

        except Exception as e:
            print("Failed to update 'SubSubCategory' information: ", e)
            return Response({"error": "Error in updating 'SubSubCategory' object"}, status.HTTP_400_BAD_REQUEST)

    def delete(self, request, **kwargs):
        try:
            sub_sub_category_obj = get_object_or_404(models.SubSubCategory, id=kwargs['subSubCategoryId'], sub_category_id=kwargs['subCategoryId'])

            sub_sub_category_obj.delete()

            return Response({"message": "Successfully deleted 'SubSubCategory' object"}, status.HTTP_204_NO_CONTENT)

        except Exception as e:
            print("Failed to delete 'SubSubCategory' information: ", e)
            return Response({"error": "Error in deleting 'SubSubCategory' object"}, status.HTTP_400_BAD_REQUEST)


class GenerateUUID(APIView):
    def get(self, request):
        try:
            new_uuid = uuid.uuid4()

            return Response(new_uuid, status.HTTP_200_OK)

        except Exception as e:
            print("Error in generating UUID ", e)
            return Response({"error": "Error in generating UUID"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class GenerateSignedURLAndStoreReference(APIView):
    permission_classes = [IsAuthenticated]
    throttle_classes = [UserRateThrottle]
    """
        # if you want to store image for a particular category
        ex: localhost:8000/api/generate-signed-url?category_id=3&filename=Aashish.jpeg&file_type=image

        # if you want to store image for a particular sub-category
        ex: localhost:8000/api/generate-signed-url?sub_category_id=3&filename=Aashish.jpeg&file_type=image

        # if you want to store image for a particular sub-sub-category
        ex: localhost:8000/api/generate-signed-url?sub_sub_category_id=3&filename=Aashish.jpeg&file_type=image

        # if you want to store document under a particular sub-sub-category
        ex: localhost:8000/api/generate-signed-url?sub_sub_category_id=3&filename=Aashish.pdf&file_type=document
    """
    def get(self, request):
        try:
            bucket_name = os.getenv('BUCKET_NAME')
            region = os.getenv('REGION')

            category_id = request.query_params.get('category_id', None)
            sub_category_id = request.query_params.get('sub_category_id', None)
            sub_sub_category_id = request.query_params.get('sub_sub_category_id', None)
            object_name = request.query_params.get('filename', 'no-file-name')
            file_type = request.query_params.get('file_type', 'document')

            if category_id:
                obj = get_object_or_404(models.Category, id=category_id)
            elif sub_category_id:
                obj = get_object_or_404(models.SubCategory, id=sub_category_id)
            elif sub_sub_category_id:
                obj = get_object_or_404(models.SubSubCategory, id=sub_sub_category_id)
            else:
                return Response({"Error": "Invalid identifier"})

            if file_type == 'document':
                prefix = 'documents/'
                content_type = 'application/pdf'
            elif file_type == 'image':
                prefix = 'images/'
                content_type = 'image/png'
            else:
                return Response({"Error": "Invalid File format"}, status.HTTP_400_BAD_REQUEST)

            object_key = f"{prefix}{object_name}"

            s3_file_url = f"https://{bucket_name}.s3.amazonaws.com/{object_key}"

            if file_type == 'image':
                obj.image_url = s3_file_url
            elif file_type == 'document':
                obj.document_url = s3_file_url

            obj.save()

            s3Client = boto3.client('s3', region_name=region)

            presigned_url = s3Client.generate_presigned_url('put_object',  # permission of this url is: only 'put' images
                                                            Params={'Bucket': bucket_name, 'Key': object_key,  # basic config.
                                                                    'ContentType': content_type},  # the content type should match both on backend and frontend
                                                            ExpiresIn=3600)  # expires in 1hr

            return Response({'url': presigned_url}, status.HTTP_200_OK)
        except Exception as e:
            print("Error in generating pre-signed URL", e)
            return Response({"Error": "Couldn't generate signed URL"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


# logic for handling user registration(OTPs) and assigning them groups
redis_url = urlparse(settings.CACHES['default']['LOCATION'])
redis_host = redis_url.hostname
redis_port = redis_url.port

redis_instance = redis.StrictRedis(host=redis_host, port=redis_port, db=0, decode_responses=True)


# generate OTP
class GenerateOTP(APIView):
    permission_classes = [AllowAny]
    throttle_classes = [AnonRateThrottle, UserRateThrottle]

    def post(self, request):
        try:
            username = request.data.get('username')
            if not username:
                return Response({"Error": "Phone number is required"}, status.HTTP_400_BAD_REQUEST)

            otp = random.randint(10000, 99999)  # 5 digit OTP (only for testing purpose)
            redis_instance.set(username, otp, ex=300)  # phone_number: otp(key-value pair). store for 300 sec

            # TODO: To send this otp to the phone_number(yet to do)
            """
            # I need a twilio phone number which is paid :( 
            client = Client(os.getenv('TWILIO_ACCOUNT_SID'), os.getenv('TWILIO_AUTH_TOKEN'))

            message = client.messages.create(
                body = f"You OTP for Ramayan book store is: {otp}",
                from_ = os.getenv('TWILIO_PHONE_NUMBER'),
                to = "+91"+username
            )
            """
            """
            sns_client = boto3.client('sns',
                                      aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
                                      aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
                                      region_name=os.getenv('AWS_REGION'))

            sns_client.publish(
                PhoneNumber="+91"+username,  # E.164 format
                Message=f"Your OTP for Ramayan book store is: {otp}",
                MessageAttributes={
                    'AWS.SNS.SMS.SMSType': {
                        'DataType': 'String',
                        'StringValue': 'Transactional'
                    }
                }
            )
            """
            print(f"OTP for {username}: {otp}")

            return Response({"message": "OTP sent successfully"}, status.HTTP_200_OK)
        except Exception as e:
            print("Error in generating OTP: ", e)
            return Response({"message": "Error in generating OTP"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


# handle registering new users
class VerifyOTPAndSignUp(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username')  # alias for phone number
            otp = request.data.get('otp')
            user_type = request.data.get('user_type', 'Customer')

            stored_otp = redis_instance.get(username)

            if not stored_otp or stored_otp != otp:
                return Response({"error": "Invalid or Expired OTP"}, status.HTTP_400_BAD_REQUEST)

            serializer = serializers.CustomUserSerializer(data=request.data, context={'user_type': user_type})

            serializer.is_valid(raise_exception=True)

            user = serializer.save()

            # TODO: After storing the user details in the DB, return JWT tokens to the client for making subsequent API calls
            refresh = RefreshToken.for_user(user)
            data = {
                'refresh': str(refresh),
                'access': str(refresh.access_token)
            }

            return Response({"message": "Successfully signed up", "tokens": data}, status.HTTP_201_CREATED)
        except Exception as e:
            print("Error in verifying OTP: ", e)
            return Response({"Error": "Server Error"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class VerifyOTPAndSignIn(APIView):
    permission_classes = [AllowAny]

    def post(self, request):
        try:
            username = request.data.get('username')  # alias for phone number
            otp = request.data.get('otp')

            stored_otp = redis_instance.get(username)

            if not stored_otp or stored_otp != otp:
                return Response({"error": "Invalid or Expired OTP"}, status.HTTP_400_BAD_REQUEST)

            user = User.objects.get(username=username)

            if user:
                refresh = RefreshToken.for_user(user)

                data = {
                    'refresh': str(refresh),
                    'access': str(refresh.access_token),
                }

                return Response({"message": "Successfully signed in", "tokens": data}, status.HTTP_200_OK)
            return Response({"Error": "User Does not exist"}, status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            print("Error in Signin process: ", e)
            return Response({"Error": "Couldn't complete sign-in process"}, status.HTTP_400_BAD_REQUEST)


class UpdateUserData(APIView):
    permission_classes = [IsAuthenticated]

    def patch(self, request):
        try:
            user = get_object_or_404(User, username=request.data.get('username'))

            serializer = serializers.CustomUserSerializer(instance=user, data=request.data, partial=True)

            serializer.is_valid(raise_exception=True)

            serializer.save()

            return Response({"Message": "success in updating user information"})
        except Exception as e:
            print("Error in updating user information: ", e)
            return Response({"Error": "error in updating user information"})
