from django.db import models


class Brand(models.Model):
    id = models.UUIDField(db_column='ID', primary_key=True)
    name = models.CharField(db_column='Name')

    class Meta:
        db_table = 'Brand'


class Model(models.Model):
    id = models.UUIDField(db_column='ID', primary_key=True)
    brand_id = models.ForeignKey(Brand, models.CASCADE, db_column='BrandID')
    name = models.CharField(db_column='Name')

    class Meta:
        db_table = 'Model'
