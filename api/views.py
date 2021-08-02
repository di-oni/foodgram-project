from django.http import request
from django.shortcuts import get_object_or_404
from recipes.models import Favourite, Follow, Ingredient, Purchase
from rest_framework import filters, mixins, status, viewsets
from rest_framework.response import Response

from .serializers import (FavouriteSerializer, FollowSerializer,
                          IngredientSerializer, PurchaseSerializer)


class IngredientViewSet(viewsets.ModelViewSet):
    """ ViewSet для модели Ingredient """
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    search_fields = ['^name']
    filter_backends = [filters.SearchFilter]


class CreateDeleteViewSet(viewsets.GenericViewSet,
                          mixins.CreateModelMixin,
                          mixins.DestroyModelMixin):
    """ Пользовательский ViewSet, наследующий GenericViewSet 
        и позволяющий создавать и удалять объекты модели """
    pass


class FollowViewSet(CreateDeleteViewSet):
    """ ViewSet для модели Ingredient, наследующий CreateDeleteView """
    queryset = Follow.objects.all()
    serializer_class = FollowSerializer

    def create(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'author': request.data['id'],
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Follow, user=request.user, author__id=self.kwargs.get('pk')
        )
        self.perform_destroy(instance)
        return Response({'success': True}, status=status.HTTP_200_OK)


class FavouriteViewSet(CreateDeleteViewSet):
    """ ViewSet для модели Favourite, наследующий CreateDeleteView """
    queryset = Favourite.objects.all()
    serializer_class = FavouriteSerializer

    def create(self, request, *args, **kwargs):
        data = {
            'user': request.user.id,
            'recipe': request.data['id'],
        }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Favourite, user=request.user, recipe__id=self.kwargs.get('pk')
        )
        self.perform_destroy(instance)
        return Response({'success': True}, status=status.HTTP_200_OK)


class PurchasesViewSet(CreateDeleteViewSet):
    """ ViewSet для модели Purchases, наследующий CreateDeleteView """
    queryset = Purchase.objects.all()
    serializer_class = PurchaseSerializer

    def create(self, request, *args, **kwargs):
        data = {
                'user': request.user.id,
                'recipe': request.data['id'],
            }
        serializer = self.get_serializer(data=data)
        serializer.is_valid(raise_exception=True)
        self.perform_create(serializer)
        headers = self.get_success_headers(serializer.data)
        return Response(serializer.data, status=status.HTTP_201_CREATED,
                        headers=headers)

    def destroy(self, request, *args, **kwargs):
        instance = get_object_or_404(
            Purchase, user=request.user, recipe__id=self.kwargs.get('pk')
        )
        self.perform_destroy(instance)
        return Response({'success': True}, status=status.HTTP_200_OK)
