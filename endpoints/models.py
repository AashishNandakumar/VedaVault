from django.db import models
from django.contrib.auth.models import AbstractUser

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
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField()


class SubCategories(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField()
    category = models.ForeignKey(Categories, on_delete=models.CASCADE, related_name='subcategories')


class SubSubCategories(models.Model):
    name = models.CharField(max_length=255)
    description = models.TextField()
    image = models.URLField()
    document = models.URLField()
    subcategory = models.ForeignKey(SubCategories, on_delete=models.CASCADE, related_name='subsubcategories')
