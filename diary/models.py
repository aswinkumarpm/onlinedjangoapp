from django.conf import settings
from django.db import models
from django.contrib.auth.models import AbstractUser


# Create your models here.

GENDER_CHOICES = (
    ('Male', 'Male'),
    ('Female', 'Female'),
)


class Registration(AbstractUser):
    name = models.CharField(max_length=100, blank=True)
    gender = models.CharField(max_length=10, choices=GENDER_CHOICES, blank=True, null=True)
    dob = models.DateField(blank=True, null=True)
    mobile_num = models.CharField(max_length=16, blank=True, null=True)
    telephone = models.CharField(max_length=15, blank=True, null=True)
    photo = models.ImageField(upload_to='pic_folder/pic/', default='/pic_folder/pic/dummy-pro-pic.png', blank=True, null=True)


    def __str__(self):
        return str(self.username)



class DiaryManager(models.Manager):
    def public(self, *args, **kwargs):
        return super(DiaryManager, self).filter(is_public=True)



class Diary(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, default=1, on_delete=models.CASCADE, blank=True, null=True)
    title = models.CharField(max_length=120)
    content = models.TextField()
    updated = models.DateTimeField(auto_now=True, auto_now_add=False)
    timestamp = models.DateTimeField(auto_now=False, auto_now_add=True)
    is_public = models.BooleanField(default=False)

    objects = DiaryManager()

    def __str__(self):
        return str(self.title)


class Contact(models.Model):
    email = models.EmailField()
    full_name = models.CharField(max_length=100, blank=False, null=True)
    message = models.CharField(max_length=100, blank=False, null=True)

    def __str__(self):
        return str(self.full_name)


