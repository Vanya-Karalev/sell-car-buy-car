from django.db import models
from users.models import CustomUser


class Brand(models.Model):
    name = models.CharField(db_column='Name')

    class Meta:
        db_table = 'Brand'

    def __str__(self):
        return self.name


class Model(models.Model):
    brand = models.ForeignKey(Brand, on_delete=models.CASCADE, db_column='BrandID')
    name = models.CharField(db_column='Name')

    class Meta:
        db_table = 'Model'

    def __str__(self):
        return self.name


class Engine(models.Model):
    type = models.CharField(db_column='Type')
    horse_power = models.IntegerField(db_column='HorsePower')
    capacity = models.FloatField(db_column='Capacity')
    torque = models.IntegerField(db_column='Torque')
    fuel_consuption = models.FloatField(db_column='FuelConsuption')

    class Meta:
        db_table = 'Engine'

    def __str__(self):
        return 'type: {}, horse power: {}'.format(self.type, self.horse_power)


class Gearbox(models.Model):
    type = models.CharField(db_column='Type')
    gear_number = models.IntegerField(db_column='GearNumber')

    class Meta:
        db_table = 'Gearbox'

    def __str__(self):
        return 'type: {}, gear number: {}'.format(self.type, self.gear_number)


class Suspension(models.Model):
    type = models.CharField(db_column='Type')
    clearance = models.FloatField(db_column='Clearance')

    class Meta:
        db_table = 'Suspension'

    def __str__(self):
        return 'type: {}, clearance: {}'.format(self.type, self.clearance)


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

    def __str__(self):
        return self.vin


class Image(models.Model):
    image = models.FileField(upload_to="images/", null=True)

    class Meta:
        db_table = 'Image'


class Ad(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='UserID')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, db_column='CarID')
    price = models.IntegerField(db_column='Price')
    description = models.CharField(db_column='Description')
    status = models.BooleanField(db_column='Status', default='False')
    images = models.ManyToManyField(Image)

    class Meta:
        db_table = 'Ad'

    def __str__(self):
        return self.price


class Favorites(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='UserID')
    ad = models.ForeignKey(Ad, on_delete=models.CASCADE, db_column='AdID')

    class Meta:
        db_table = 'Favorites'

    def __str__(self):
        return f"{self.user.username}'s Favorite: {self.ad}"


class Bid(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='UserID')
    amount = models.IntegerField(db_column='Amount')
    date = models.DateTimeField(db_column='Date')

    class Meta:
        db_table = 'Bid'


class Auction(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, db_column='UserID')
    car = models.ForeignKey(Car, on_delete=models.CASCADE, db_column='CarID')
    start_price = models.IntegerField(db_column='StartPrice')
    start_date = models.DateTimeField(db_column='StartDate')
    end_date = models.DateTimeField(db_column='EndDate')
    description = models.CharField(db_column='Description')
    bid = models.ForeignKey(Bid, on_delete=models.DO_NOTHING, db_column='BidID', blank=True, null=True)
    images = models.ManyToManyField(Image)

    class Meta:
        db_table = 'Auction'

    def __str__(self):
        return self.start_date
