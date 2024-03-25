from django.urls import path, include
from rest_framework.routers import DefaultRouter

from . import views2
from .views2 import CategoryViewSet, SubCategoryViewSet, SubSubCategoryViewSet

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'subsubcategories', SubSubCategoryViewSet)

urlpatterns = [
    path('admin-signup', views2.AdminSignup.as_view()),
    path('admin-signin', views2.AdminSignin.as_view()),
    path('generate-otp', views2.OTPGenerator.as_view()),
    path('verify-otp', views2.OTPVerifier.as_view()),
    path('admin-reset-password', views2.AdminResetPassword.as_view()),
    path('generate-file-url', views2.S3UploadView.as_view()),
    path('get-phone-number', views2.UserInformation.as_view()),
    path('', include(router.urls))
]
