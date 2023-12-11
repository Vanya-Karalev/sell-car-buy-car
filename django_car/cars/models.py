from django.db import models
from users.models import CustomUser


class Brand(models.Model):
    name = models.CharField(db_column='Name')

    class Meta:
        db_table = 'Brand'


class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_column='BrandID')
    name = models.CharField(db_column='Name')

    class Meta:
        db_table = 'Model'


class Engine(models.Model):
    type = models.CharField(db_column='Type')
    horse_power = models.IntegerField(db_column='HorsePower')
    capacity = models.FloatField(db_column='Capacity')
    torque = models.IntegerField(db_column='Torque')
    fuel_consuption = models.FloatField(db_column='FuelConsuption')

    class Meta:
        db_table = 'Engine'


class Gearbox(models.Model):
    type = models.CharField(db_column='Type')
    gear_number = models.IntegerField(db_column='GearNumber')

    class Meta:
        db_table = 'Gearbox'


class Suspension(models.Model):
    type = models.CharField(db_column='Type')
    clearance = models.FloatField(db_column='Clearance')

    class Meta:
        db_table = 'Suspension'


class Car(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_column='BrandID')
    model = models.ForeignKey(Model, on_delete=models.CASCADE, db_column='ModelID')
    engines = models.ManyToManyField(Engine)
    gearboxes = models.ManyToManyField(Gearbox)
    suspensions = models.ManyToManyField(Suspension)
    mileage = models.IntegerField(db_column='Mileage')
    body_type = models.CharField(db_column='BodyType')
    year = models.IntegerField(db_column='Year')
    color = models.CharField(db_column='Color')
    vin = models.CharField(db_column='VIN')

    class Meta:
        db_table = 'Car'


class Ad(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='UserID')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, db_column='CarID')
    price = models.IntegerField(db_column='Price')
    description = models.CharField(db_column='Description')
    status = models.BooleanField(db_column='Status', default='False')

    class Meta:
        db_table = 'Ad'
