from django.urls import include, path
from rest_framework.routers import DefaultRouter

from .views import (FavouriteViewSet, FollowViewSet, IngredientViewSet,
                    PurchasesViewSet)

router = DefaultRouter() 

router.register(r'ingredients', IngredientViewSet, basename='ingredients')
router.register(r'favorites', FavouriteViewSet, basename='favorites')
router.register(r'purchases', PurchasesViewSet, basename='purchases')
router.register(r'subscriptions', FollowViewSet, basename='subscriptions')

urlpatterns = [
    path('v1/', include(router.urls)),
]
