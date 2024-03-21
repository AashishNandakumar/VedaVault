from django.urls import path
from . import views

# All you backend endpoints go here
urlpatterns = [
    # API version 1
    path("generate-otp", views.GenerateOTP.as_view()),  # POST. send phone_no as payload and get an OTP
    path("verify-otp-signup", views.VerifyOTPAndSignUp.as_view()),  # POST. send phone_no, OTP, first_name, last_name, email as payload, get validated, and you will get a pair of tokens
    path("verify-otp-signin", views.VerifyOTPAndSignIn.as_view()),  # POST. send phone_no and OTP as payload, get validated, and you will get a pair of tokens
    path("update-user-data", views.UpdateUserData.as_view()),  # PATCH. Update user info

    path("categories", views.CategoryBulk.as_view()),  # GET, POST. Fetch and Add Categories
    path("categories/<int:categoryId>", views.CategoryParticular.as_view()),  # DELETE, PATCH. Delete and Update Categories
    path("category/<int:categoryId>/sub-category", views.SubCategoryBulk.as_view()),  # GET, POST. Fetch and Add SubCategories
    path("category/<int:categoryId>/sub-category/<int:subCategoryId>", views.SubCategoryParticular.as_view()),  # DELETE, PATCH. Delete and Update SubCategories
    path("category/<int:categoryId>/sub-category/<int:subCategoryId>/sub-sub-category", views.SubSubCategoryBulk.as_view()),  # GET, POST. Fetch and Add SubSubCategories
    path("category/<int:categoryId>/sub-category/<int:subCategoryId>/sub-sub-category/<int:subSubCategoryId>", views.SubSubCategoryParticular.as_view()),  # DELETE, PATCH. Delete and Update SubSubCategories

    path("generate-uuid", views.GenerateUUID.as_view()),  # GET. Fetch UUID to rename the files from the client(so that every filename in S3 is unique)
    path("generate-signed-url-and-store-reference", views.GenerateSignedURLAndStoreReference.as_view()),  # GET. Fetch signed URL, push the file to S3, give back the file details to backend so that it stores the reference to S3

    # API version 2

]
