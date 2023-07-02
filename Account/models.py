from django.db import models
from django.contrib.auth.models import AbstractUser
from django.contrib.auth.models import BaseUserManager, AbstractBaseUser
# Create your models here.
class UserManager(BaseUserManager):
    def create_user(self, name, username,email,password = None):
        user = self.model(
            email=self.normalize_email(email),
            username = username,
            name = name

        )
        user.set_password(password)
        user.is_active = True
        user.save()
        return user
    def create_superuser(self, username, email, password=None,**extra_kwargs):
        user = self.model(
            email=self.normalize_email(email),
            username = username,
        )
        user.is_admin = True
        user.is_superuser = True
        user.set_password(password)
        user.save()
        print(user.is_admin)
        return user

class User(AbstractUser):
    name = models.CharField(max_length=256)
    username = models.CharField(max_length=256, null=True)
    email = models.EmailField(max_length=256,unique=True)
    password = models.CharField(max_length=256)
    # is_staff = models.BooleanField(default=False)
    is_admin = models.BooleanField(default=False)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']
    objects = UserManager()


    def __str__(self) -> str:
        return self.email

    @property
    def is_staff(self):
        return self.is_admin
    

class product(models.Model):
    title = models.CharField(max_length=256,null=True, blank=True)


    def __str__(self) -> str:
        return self.title