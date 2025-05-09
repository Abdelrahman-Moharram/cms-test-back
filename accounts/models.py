from django.db import models
from django.contrib.auth.models import (
    BaseUserManager,
    AbstractBaseUser,
    PermissionsMixin
)
from project.models import BaseModel, BaseModelManager
import uuid
from django.conf import settings
from roles.models import Role

class UserAccountManager(BaseUserManager):
    def create_user(self, full_name, username, **kwargs):
        if not full_name:
            raise ValueError('Users must have an full name')

        username = username.lower()
        user = self.model(
            username=username,
            full_name=full_name,
            **kwargs
        )

        # user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, full_name, username, password=None, **kwargs):
        user = self.create_user(
            full_name,
            username,
            password=password,
            **kwargs
        )

        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user




class  UserType(BaseModel):
    name                = models.CharField(max_length=50)
    
    objects = BaseModelManager()
    def __str__(self):
        return self.name
    



class User(AbstractBaseUser, PermissionsMixin):
    
    id                  = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    full_name           = models.CharField(max_length=255)
    username            = models.CharField(max_length=255, unique=True)

    # image               = models.ImageField(default="users/default.jpg",upload_to=imagesave, null=True)

    is_active           = models.BooleanField(default=True)
    is_staff            = models.BooleanField(default=False)
    is_superuser        = models.BooleanField(default=False)

    role                = models.ForeignKey(Role, related_name='users', null=True, on_delete=models.SET_NULL)
    user_type           = models.ForeignKey(UserType, blank=True, null=True, on_delete=models.SET_NULL)
    
    created_at          = models.DateTimeField(auto_now=False, auto_now_add=True)
    last_update_at      = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)
    last_delete_at      = models.DateTimeField(auto_now=False, auto_now_add=False, null=True, blank=True)

    
    created_by          = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, related_name='user_created_by', on_delete=models.SET_NULL)
    updated_by          = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='user_updated_by', on_delete=models.SET_NULL)
    deleted_by          = models.ForeignKey(settings.AUTH_USER_MODEL, null=True, blank=True, related_name='user_deleted_by', on_delete=models.SET_NULL)
    
    objects = UserAccountManager()
    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['full_name']

    def __str__(self):
        return self.full_name
    
    def save(self, *args, **kwargs):
        user = super(User, self)
        if not (user.is_superuser):
            user.set_password(self.password)
        super().save(*args, **kwargs)
        return user

