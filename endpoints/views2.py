import boto3
from django.conf import settings
from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework import viewsets
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers2
from .models import Categories, SubCategories, SubSubCategories

User = get_user_model()


class AdminSignup(APIView):

    def post(self, request):
        """
        :param request: 'username', 'phone_number', 'password'
        :return: Success ? Tokens : Error Message
        """
        try:
            serializer = serializers2.AdminSignupSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            user = serializer.save()

            refresh = RefreshToken.for_user(user)

            return Response({
                "Success": "Success in 'Admin-Signup'",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            },
                status.HTTP_201_CREATED
            )
        except Exception as e:
            print("Error while 'Admin-Signup': ", e)

            return Response({"Error": "Error while 'Admin-Signup'"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminSignin(APIView):

    def post(self, request):
        """
        :param request: 'username', 'password'
        :return: success ? Tokens : Error Message /direct to forgot password
        """
        try:
            serializer = serializers2.AdminSigninSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.get('user')

            refresh = RefreshToken.for_user(user)

            return Response(
                {"Success": "Successfully Signed-In", "refresh": str(refresh), "access": str(refresh.access_token)},
                status.HTTP_200_OK)

        except Exception as e:
            print("Error while 'Admin-Signin': ", e)
            return Response({"Error": "Error while 'Admin-Signin'"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


"""
class AdminForgotPassword(APIView):

    def post(self, request):
        
        try:
            serializer = serializers2.AdminForgotPasswordSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            otp = serializer.validated_data.get('otp')  # only for testing purpose

            return Response({"Success": f"Successfully generated OTP for 'Password' reset - {otp}"},
                            status.HTTP_201_CREATED)
        except Exception as e:
            print("Error while 'Generating-OTP': ", e)
            return Response({"Error": "Failed to generate OTP"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
"""


class OTPGenerator(APIView):
    def post(self, request):
        try:
            serializer = serializers2.OTPGeneratorSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)

            username = serializer.validated_data.get('username')
            phone_number = serializer.validated_data.get('phone_number')
            otp = serializer.validated_data.get('otp')

            print(f"OTP for phone number {phone_number} for user {username} is:  {otp}")
            return Response({"Success": f"OTP for {phone_number} is {otp}"})
        except Exception as e:
            print("Error occurred while generating OTP: ", e)
            return Response({"Error": "Failed to generate OTP"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class OTPVerifier(APIView):
    def post(self, request):
        try:
            serializer = serializers2.OTPVerifierSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            status_msg = serializer.validated_data.get('status')

            return Response({"Success": "Successfully verified OTP", "status": status_msg})
        except Exception as e:
            print("Error occurred while verifying OTP: ", e)
            return Response({"Error": "Failed to verify OTP"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminResetPassword(APIView):

    def post(self, request):
        """
        :param request: 'username', 'new_password'
        :return: Success ? Tokens : Error Message
        """
        try:
            serializer = serializers2.AdminResetPasswordSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            user = serializer.validated_data.get('user')

            refresh = RefreshToken.for_user(user)
            return Response({
                "Success": "Success in 'Resetting Admin Password'",
                "refresh": str(refresh),
                "access": str(refresh.access_token)
            },
                status.HTTP_201_CREATED
            )
        except Exception as e:
            print("Error while Resetting Admin Password: ", e)
            return Response({"Error": "Failed to Reset Admin Password"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class S3UploadView(APIView):
    def post(self, request):
        file_obj = request.data.get('file')
        file_type = file_obj.content_type

        s3Client = boto3.client('s3',
                                aws_access_key_id=settings.AWS_ACCESS_KEY_ID,
                                aws_secret_access_key=settings.AWS_SECRET_ACCESS_KEY,
                                region_name=settings.AWS_S3_REGION_NAME)

        bucket_name = settings.AWS_S3_BUCKET_NAME
        file_name = file_obj.name
        key = f"uploads/{file_name}"

        print(settings.AWS_ACCESS_KEY_ID)
        s3Client.upload_fileobj(file_obj, bucket_name, key, ExtraArgs={'ContentType': file_type})

        file_url = f"https://{bucket_name}.s3.amazonaws.com/{key}"

        return Response({'file_url': file_url}, status.HTTP_201_CREATED)


class CategoryViewSet(viewsets.ModelViewSet):
    queryset = Categories.objects.all()
    serializer_class = serializers2.CategorySerializer


class SubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubCategories.objects.all()
    serializer_class = serializers2.SubCategorySerializer


class SubSubCategoryViewSet(viewsets.ModelViewSet):
    queryset = SubSubCategories.objects.all()
    serializer_class = serializers2.SubSubCategorySerializer
