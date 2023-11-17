# Importing necessary modules from Django
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext as _

# Creating a custom user manager for the Client model
class ClientManager(BaseUserManager):
    # Method to create a regular user
    def create_user(self, userid, password=None, **extra_fields):
        if not userid:
            raise ValueError('The User ID field must be set')
        # Creating a new user instance
        user = self.model(userid=userid, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # Method to create a superuser
    def create_superuser(self, userid, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(userid, password, **extra_fields)

# Custom user model inheriting from AbstractUser and PermissionsMixin
class Client(AbstractUser, PermissionsMixin):
    # Custom field for User ID with max length 12, acting as the primary key
    userid = models.CharField(max_length=12, primary_key=True)
    # Additional fields like username, first_name, last_name, etc.
    username = models.CharField(max_length=12, default='user')
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    usertype = models.CharField(max_length=30, blank=False)
    phone_number = models.CharField(max_length=17, blank=True)
    email = models.EmailField(unique=False, blank=False)
    company = models.CharField(max_length=100, blank=True)
    address = models.TextField(max_length=300, blank=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    # Using the custom manager defined above
    objects = ClientManager()

    # Specifying the field to be used as the username for authentication
    USERNAME_FIELD = 'userid'
    # Additional required fields for creating a user
    REQUIRED_FIELDS = ['first_name', 'last_name', 'email', 'usertype']

    # Many-to-Many relationship with Groups and Permissions
    groups = models.ManyToManyField(
        Group,
        verbose_name=_('groups'),
        blank=True,
        related_name='client_set',  # Added related_name
        related_query_name='client',
    )

    user_permissions = models.ManyToManyField(
        Permission,
        verbose_name=_('user permissions'),
        blank=True,
        related_name='client_set',  # Added related_name
        related_query_name='client',
    )

    # A string representation of the user (in this case, the User ID)
    def __str__(self):
        return self.userid

