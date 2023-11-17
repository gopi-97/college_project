# Importing necessary modules from Django
from django.contrib.auth.models import AbstractUser, PermissionsMixin, BaseUserManager, Group, Permission
from django.db import models
from django.utils.translation import gettext as _
import random,string
# Creating a custom user manager for the Client model
class ClientManager(BaseUserManager):
    # Method to create a regular user
    def create_user(self, password=None, **extra_fields):
        extra_fields['userid'] = self.generate_unique_userid()  # Generating a unique 6-character ID if not provided
        user = self.model(**extra_fields)
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

        return self.create_user(password=password, **extra_fields)
    
    
    def generate_unique_userid(self):
        while True:
            # Generating a random 6-character ID
            unique_id = ''.join(random.choices(string.ascii_uppercase + string.digits, k=6))
            if not self.model.objects.filter(userid=unique_id).exists():
                return unique_id

# Custom user model inheriting from AbstractUser and PermissionsMixin
class Client(AbstractUser, PermissionsMixin):
    # Custom field for User ID  
    userid = models.CharField(max_length=6, unique=True,primary_key=True)

    # Additional fields 
    full_name = models.CharField(max_length=300, blank=True)

    # When using choices in Django's model field, it should be a list of tuples, 
    # #where each tuple contains two elements: the actual value to be stored in the database and a human-readable name
    USER_TYPES = [
    ('Farmer', 'Farmer'),
    ('Merchant', 'Merchant'),
]
    usertype = models.CharField(choices=USER_TYPES, blank=False,max_length=50)

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
    REQUIRED_FIELDS = ['full_name', 'email', 'usertype']

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

