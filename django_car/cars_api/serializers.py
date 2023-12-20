from rest_framework import serializers
from users.models import CustomUser
from cars.models import Ad, Auction, Favorites, Image, Car, Brand, Model, Engine, Gearbox, Suspension


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'phone', 'password']


class AdSerializer(serializers.ModelSerializer):
    class Meta:
        model = Ad
        fields = '__all__'


class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = '__all__'


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = ['id', 'image']


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)

    class Meta:
        model = Model
        fields = ['id', 'brand', 'name']


class EngineSerializer(serializers.ModelSerializer):
    class Meta:
        model = Engine
        fields = '__all__'


class GearboxSerializer(serializers.ModelSerializer):
    class Meta:
        model = Gearbox
        fields = '__all__'


class SuspensionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Suspension
        fields = '__all__'


class CarSerializer(serializers.ModelSerializer):
    brand = BrandSerializer(read_only=True)
    model = ModelSerializer(read_only=True)
    engines = EngineSerializer(many=True, read_only=True)
    gearboxes = GearboxSerializer(many=True, read_only=True)
    suspensions = SuspensionSerializer(many=True, read_only=True)

    class Meta:
        model = Car
        fields = ['id', 'brand', 'model', 'engines', 'gearboxes', 'suspensions', 'mileage', 'body_type', 'year', 'color', 'vin']


class AdImgSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True, read_only=True)
    car = CarSerializer(read_only=True)
    user = CustomUserSerializer(read_only=True)

    class Meta:
        model = Ad
        fields = ['id', 'price', 'description', 'status', 'user', 'car', 'images']
