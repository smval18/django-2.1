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
    image_admin = models.ImageField(verbose_name="изображение готового дизайна", upload_to='images_admin',
                                    help_text="добавить изображение при смене статуса на выполнено", blank=True)
    comment_admin = models.TextField(verbose_name="комментарий",
                                     help_text="добавить комментарий при смене статуса на принят в работу", blank=True)

    @staticmethod
    def get_count():
        return Application.objects.count()

    @staticmethod
    def get_new_applications():

        return Application.objects.filter(status=Status.objects.get(name='новая')).order_by('created_at')[:4]

    @staticmethod
    def get_accept_applications():
        return Application.objects.filter(status=Status.objects.get(name='принята в работу')).order_by('created_at')[:4]

    @staticmethod
    def get_accept_applications_count():
        return Application.objects.filter(status=Status.objects.get(name='принята в работу')).count()

    @staticmethod
    def get_done_applications():
        return Application.objects.filter(status=Status.objects.get(name='выполнено')).order_by('created_at')[:4]


    def __str__(self) -> str:
        return self.name
