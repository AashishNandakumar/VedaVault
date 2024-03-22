from django.urls import path, include
from .views2 import CategoryViewSet, SubCategoryViewSet, SubSubCategoryViewSet
from rest_framework.routers import DefaultRouter

from . import views2

router = DefaultRouter()
router.register(r'categories', CategoryViewSet)
router.register(r'subcategories', SubCategoryViewSet)
router.register(r'subsubcategories', SubSubCategoryViewSet)

urlpatterns = [
    path('admin-signup', views2.AdminSignup.as_view()),
    path('admin-signin', views2.AdminSignin.as_view()),
    path('admin-forgot-password', views2.AdminForgotPassword.as_view()),
    path('admin-reset-password', views2.AdminResetPassword.as_view()),
    path('', include(router.urls))
]
