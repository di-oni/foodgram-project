from django.http import request
from django.shortcuts import get_object_or_404
from rest_framework import filters, status, viewsets
from rest_framework.response import Response

from recipes.models import (Favourite, Follow, Ingredient, Purchase, Recipe,
                            User)

from .mixins import CreateDeleteViewSet
from .serializers import (FavouriteSerializer, FollowSerializer,
                          IngredientSerializer, PurchaseSerializer)


class IngredientViewSet(viewsets.ModelViewSet):
    """ ViewSet для модели Ingredient """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ["^name"]
    filter_backends = [filters.SearchFilter]


class FollowViewSet(CreateDeleteViewSet):
    """ ViewSet для модели Ingredient, наследующий CreateDeleteView """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def perform_create(self, serializer):
        author = get_object_or_404(User, id=self.request.data["id"])
        serializer.save(user=self.request.user, author=author)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Follow, user=request.user, author__id=self.kwargs.get("pk")
        )
        self.perform_destroy(instance)
        return Response({"success": True}, status=status.HTTP_200_OK)


class FavouriteViewSet(CreateDeleteViewSet):
    """ ViewSet для модели Favourite, наследующий CreateDeleteView """
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.request.data["id"])
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Favourite, user=request.user, recipe__id=self.kwargs.get("pk")
        )
        self.perform_destroy(instance)
        return Response({"success": True}, status=status.HTTP_200_OK)


class PurchasesViewSet(CreateDeleteViewSet):
    """ ViewSet для модели Purchases, наследующий CreateDeleteView """
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def perform_create(self, serializer):
        recipe = get_object_or_404(Recipe, id=self.request.data["id"])
        serializer.save(user=self.request.user, recipe=recipe)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Purchase, user=request.user, recipe__id=self.kwargs.get("pk")
        )
        self.perform_destroy(instance)
        return Response({"success": True}, status=status.HTTP_200_OK)
