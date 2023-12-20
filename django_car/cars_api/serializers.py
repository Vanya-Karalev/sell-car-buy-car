from rest_framework import serializers
from users.models import CustomUser
from cars.models import Ad, Auction, Favorites, Image, Car, Brand, Model, Engine, Gearbox, Suspension


class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = CustomUser
        fields = ['username', 'email', 'first_name', 'phone', 'password']


class ImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = Image
        fields = '__all__'


class BrandSerializer(serializers.ModelSerializer):
    class Meta:
        model = Brand
        fields = '__all__'


class ModelSerializer(serializers.ModelSerializer):
    brand = BrandSerializer()

    class Meta:
        model = Model
        fields = '__all__'


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
    brand = BrandSerializer()
    model = ModelSerializer()
    engines = EngineSerializer(many=True)
    gearboxes = GearboxSerializer(many=True)
    suspensions = SuspensionSerializer(many=True)

    class Meta:
        model = Car
        fields = '__all__'


class AdSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    car = CarSerializer()
    user = CustomUserSerializer()

    class Meta:
        model = Ad
        fields = '__all__'


class AuctionSerializer(serializers.ModelSerializer):
    images = ImageSerializer(many=True)
    car = CarSerializer()
    user = CustomUserSerializer()

    class Meta:
        model = Auction
        fields = '__all__'


# class FavoritesSerializer(serializers.ModelSerializer):
#     user = CustomUserSerializer(read_only=True)
#     ad = AdSerializer(many=True, read_only=True)
#
#     class Meta:
#         model = Favorites
#         fields = ['id', 'user', 'ad']

