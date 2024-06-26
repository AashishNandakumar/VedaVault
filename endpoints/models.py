from django.contrib.auth.models import AbstractUser
from django.db import models

"""
class Category(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    image_url = models.CharField(max_length=500, default='/no-url')  # s3 object link

    def __str__(self):
        return self.name


class SubCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    category = models.ForeignKey(Category, on_delete=models.CASCADE, default=3)  # null=True only for debugging
    image_url = models.CharField(max_length=500, default='/no-url')  # s3 object link

    def __str__(self):
        return self.name


class SubSubCategory(models.Model):
    name = models.CharField(max_length=100, unique=True)
    description = models.TextField()
    sub_category = models.ForeignKey(SubCategory, on_delete=models.CASCADE, default=9)  # null=True only for debugging
    image_url = models.CharField(max_length=500, default='/no-image-url')  # s3 object link to image
    document_url = models.CharField(max_length=500, default='/no-doc-url') # s3 object link to document

    def __str__(self):
        return self.name
"""


class CustomUser(AbstractUser):
    phone_number = models.CharField(max_length=20)

    groups = models.ManyToManyField(
        'auth.Group',
        related_name='customuser_set',
        blank=True,
        help_text='The groups this user belongs to',
        verbose_name='groups',
    )

    user_permissions = models.ManyToManyField(
        'auth.Permission',
        related_name='customuser_set',
        blank=True,
        help_text='Specific permissions for this user',
        verbose_name='user permissions',

    )


class Categories(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField()
    image = models.FileField(upload_to='category_images/')


class SubCategories(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField()
    image = models.FileField(upload_to='subcategory_images/')
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='subcategories')


class SubSubCategories(models.Model):
    name = models.CharField(max_length=255, primary_key=True)
    description = models.TextField()
    image = models.FileField(upload_to='subsubcategory_images/')
    document = models.FileField(upload_to='subsubcategory_documents/')
    subcategory = models.ForeignKey(SubCategories, on_delete=models.CASCADE, related_name='subsubcategories')


class Books(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    price = models.FloatField()
    image = models.FileField(upload_to='books_images/')

    # TODO: dealing with the book object
