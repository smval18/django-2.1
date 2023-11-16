from django.contrib.auth.models import AbstractUser
from django.db import models


class User(AbstractUser):
    middle_name = models.CharField('Middle Name', max_length=100)

    def __str__(self) -> str:
        return self.username

class Status(models.Model):
    name = models.CharField('Name', max_length=100)

    @staticmethod
    def get_by_name(name):
        return Status.objects.get(name=name)

    def __str__(self) -> str:
        return self.name


class Category(models.Model):
    name = models.CharField('Name', max_length=100)

    def __str__(self) -> str:
        return self.name


class Application(models.Model):

    name = models.CharField('Name', max_length=200)
    description = models.CharField('Description', max_length=2000)
    image = models.ImageField('Image', upload_to='images')
    status = models.ForeignKey(Status, on_delete=models.CASCADE)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    created_at = models.DateTimeField(auto_now_add=True)

    @staticmethod
    def get_count():
        return Application.objects.count()

    @staticmethod
    def get_new_applications():
        return Application.objects.filter(status=Status.objects.get(name='New')).order_by('created_at')[:4]

    @staticmethod
    def get_accept_applications():
        return Application.objects.filter(status=Status.objects.get(name='Accept')).order_by('created_at')[:4]

    @staticmethod
    def get_accept_applications_count():
        return Application.objects.filter(status=Status.objects.get(name='Accept')).count()

    @staticmethod
    def get_done_applications():
        return Application.objects.filter(status=Status.objects.get(name='Done')).order_by('created_at')[:4]

    def __str__(self) -> str:
        return self.name
