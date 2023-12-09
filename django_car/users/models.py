from django.db import models
from django.contrib.auth.models import AbstractUser


class Role(models.Model):
    id = models.UUIDField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name')

    class Meta:
        db_table = 'Role'


class CustomUser(AbstractUser):
    role_id = models.ForeignKey(Role, models.CASCADE, db_column='RoleID', default='201edf14-4ad1-446c-9d5a-effde21c2fe6')
    phone = models.CharField(db_column='Phone')
