from typing import Any
from django.contrib.auth.models import AbstractBaseUser,PermissionsMixin
from django.contrib.auth.models import UserManager
from django.db import models
from django.utils import timezone

class FarmerManager(UserManager):

    def _create_user(self, username: str, password: str | None = ..., **extra_fields: Any) -> Any:
        if not username:
            raise ValueError('username not provided')
        
        # email = self.normalize_email(email)
        user = self.model(username=username,**extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        
        return user
    
    def create_user(self,username=None,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',False)#setting default value of is_staff as False so that regular user doesnt become staff
        extra_fields.setdefault('is_superuser',False)
        return self._create_user(username,password,**extra_fields)

    def create_superuser(self,username=None,password=None,**extra_fields):
        extra_fields.setdefault('is_staff',True)
        extra_fields.setdefault('is_superuser',True)
        return self._create_user(username,password,**extra_fields)
    

class Farmer(AbstractBaseUser,PermissionsMixin):
    username = models.CharField(primary_key=True,max_length=12,unique=True,blank=False)
    profile_pic = models.ImageField(upload_to='manage_account/images/profile_pic')
    full_name = models.CharField(max_length=30, blank=False)
    phone_number = models.CharField(max_length=17, blank=True)
    email = models.EmailField(unique=False, blank=False)
    company = models.CharField(max_length=100, blank=True)
    address = models.TextField(max_length=300, blank=True)

    is_active = models.BooleanField(default=True)#newly created user will be active so that they can login without the procedure
    is_superuser = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)
    last_login = models.DateTimeField(blank=True,null=True)

    objects = FarmerManager()# whenever we use the Objects. method to access db_data then django overrides default objects with this one
    USERNAME_FIELD ='username'
    EMAIL_FIELD ='email'
    REQUIRED_FIELDS = ['full_name','email']

    class Meta:
        verbose_name = 'Farmer'
        verbose_name_plural = 'Farmers'

    def get_full_name(self):
        return self.full_name
    
    def get_short_name(self):
        return self.full_name or self.email.split('@')[0]
    
    def __str__(self) -> str:
       return self.username
    