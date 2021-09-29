from django.db import models
from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, \
                                                        PermissionsMixin
"""Create User Manager Class"""


class UserManager(BaseUserManager):

    """password=None in case you want to create a user that
    is not active that has no password
    **extra_fields => take any of the extra functions that
    are passed in when you
    call the create_user and pass them into extra fields
    => if we add new fields we just add them adhoc to our model"""
    def create_user(self, email, password=None, **extra_fields):
        """Creates and saves a new user
        => it will pass the email first and then it
        will pass anything extra we add"""
        if not email:
            raise ValueError("Users must have an email-address.")
        """writing self.model is effectively the same
        than creating a new user model"""
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Creates and saves a new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


"""This gives us all the features which come out
of the box with the Django user model
and we can build on top of them and customize it
to support our email address."""


class User(AbstractBaseUser, PermissionsMixin):
    """Custom user model that supports using email instead of username
    => max-length is 255 and the address must be unique"""
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    """Allows us to deactivate users if we have an is_active field"""
    is_active = models.BooleanField(default=True)
    """Regular users are not stuff"""
    is_staff = models.BooleanField(default=False)

    """Assign the UserManager to the objects attribute"""
    objects = UserManager()

    """Customization that we can use an email address as a username"""
    USERNAME_FIELD = "email"
