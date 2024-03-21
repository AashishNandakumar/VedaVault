"""
server URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

"""
from drf_spectacular.views import SpectacularAPIView,SpectacularSwaggerView
from rest_framework.routers import DefaultRouter
from django.contrib import admin
from django.urls import path
from django.urls import re_path
from endpoints.views import SubSubCategoryViewSet
from . import views


router=DefaultRouter()
router.register('subsubcategory',SubSubCategoryViewSet)
urlpatterns = [
    path("admin/", admin.site.urls),
    re_path('login',views.login),
    re_path('signup',views.signup),
    re_path('test_token',views.test_token),
    re_path('api/docs/schema/',SpectacularAPIView.as_view(),name='apischema'),
    re_path('api/docs/ui/',SpectacularSwaggerView.as_view()),
]+router.urls
"""


# code by Aashish
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework import permissions
from drf_yasg.views import get_schema_view
from drf_yasg import openapi


schema_view = get_schema_view(
    openapi.Info(
        title="SF Webmasters API",
        default_version='v1',
        description="Ramayan Book Store APIs",
        terms_of_service='NA',
        contact=openapi.Contact(email="aashishnkumar@gmail.com"),
        license=openapi.License(name="MIT License"),

    ),
    public=True,
    permission_classes=[permissions.AllowAny],
)

urlpatterns = [
    path("admin/", admin.site.urls),

    re_path(r'^swagger(?P<format>\.json|\.yaml)$', schema_view.without_ui(cache_timeout=0), name='schema-json'),
    path('docs/', schema_view.with_ui('swagger', cache_timeout=0), name='schema-swagger'),
    path('docs/redoc/', schema_view.with_ui('redoc', cache_timeout=0), name='schema-redoc'),

    path("v1/", include("endpoints.urls")),  # handle all custom endpoints in the 'endpoints' app itself
    path("v2/", include("endpoints.urls2")),
    # path("auth/", include("djoser.urls")),  # Djoser: library that provides ready to use endpoints for authentication
    # path("auth/", include("djoser.urls.jwt"))  # Djoser: library that provides ready to use endpoints for authentication

]

"""
djoser endpoints

(DON'T USE THESE ENDPOINTS, USE ONLY WHEN THE DEVELOPER INSTRUCTS YOU TO !!!!):

1. http://localhost:8080/auth/users/ --> In the body add username, first_name, last_name(JSON) and send a POST req to register user
    
2. http://localhost:8000/auth/jwt/create/ --> In the body add username and password(JSON) and send a POST req to generate refresh and access tokens

3.(YOU CAN USE THIS) http://localhost:8000/auth/jwt/refresh/ --> In the body add refresh: refresh_token(JSON) and send a POST req to generate access tokens
     
3. http://localhost:8000/auth/users/ --> in the header add 'Authorization: Bearer ur_token'(key-value) and send a GET req to fetch user creds

"""
