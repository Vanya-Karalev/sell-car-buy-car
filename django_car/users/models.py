from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    name = models.CharField(db_column='Name')

    class Meta:
        db_table = 'Role'


class CustomUser(AbstractUser):
    role = models.ForeignKey(Role, models.CASCADE, db_column='RoleID', default=1)
    phone = models.CharField(db_column='Phone')
