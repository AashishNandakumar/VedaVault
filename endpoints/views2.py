from django.contrib.auth import get_user_model
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework_simplejwt.tokens import RefreshToken

from . import serializers2

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


class AdminForgotPassword(APIView):

    def post(self, request):
        """
        :param request: 'username'
        :return: Generates OTP
        """
        try:
            serializer = serializers2.AdminForgotPasswordSerializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            otp = serializer.validated_data.get('otp')  # only for testing purpose

            return Response({"Success": f"Successfully generated OTP for 'Password' reset - {otp}"}, status.HTTP_201_CREATED)
        except Exception as e:
            print("Error while 'Generating-OTP': ", e)
            return Response({"Error": "Failed to generate OTP"}, status.HTTP_500_INTERNAL_SERVER_ERROR)


class AdminResetPassword(APIView):

    def post(self, request):
        """
        :param request: 'username', 'otp', 'new_password'
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
            print("Error while verifying OTP: ", e)
            return Response({"Error": "Failed to verify OTP"}, status.HTTP_500_INTERNAL_SERVER_ERROR)
