from rest_framework import serializers

from recipes.models import Favourite, Follow, Ingredient, Purchase


class IngredientSerializer(serializers.ModelSerializer):
    """ Serializer для модели Ingredient """
    class Meta:
        model = Ingredient
        fields = "__all__" 


class FavouriteSerializer(serializers.ModelSerializer):
    """ Serializer для модели Favourite """
    class Meta:
        model = Favourite
        fields = "__all__"
        read_only_fields = ["user", "recipe"]


class FollowSerializer(serializers.ModelSerializer):
    """ Serializer для модели Follow """
    class Meta:
        model = Follow
        fields = "__all__"
        read_only_fields = ["user", "author"]


class PurchaseSerializer(serializers.ModelSerializer):
    """ Serializer для модели Purchase """
    class Meta:
        model = Purchase
        fields = "__all__"
        read_only_fields = ["user", "recipe"]