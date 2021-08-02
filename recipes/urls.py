from django.urls import include, path

from . import views

profile_urls = [
    path("<str:username>/", views.view_profile, name="profile"),
]


recipe_urls = [
    path("<int:recipe_id>/", views.view_recipe, name="view_recipe"),
    path("<int:recipe_id>/edit/", views.edit_recipe, name="edit_recipe"),
    path("<int:recipe_id>/delete/", views.delete_recipe, name="delete_recipe"),
]


urlpatterns = [ 
    path("", views.index, name="index"),
    path("new/", views.new_recipe, name="new_recipe"),
    path("subscriptions/", views.subscriptions, name="subscriptions"),
    path("favorites/", views.favourites, name="favorites"),
    path("purchases/", views.purchases, name="purchases"),
    path("purchases/print_pdf/", views.print_pdf, name="print_pdf"),
    path("purchases/<int:recipe_id>/delete/", views.delete_purchase,
         name="delete_purchase"),
    path("profiles/", include(profile_urls)),
    path("recipes/", include(recipe_urls)), 
]
