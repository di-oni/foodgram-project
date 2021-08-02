from django.contrib import admin

from .models import (Favourite, Follow, Ingredient, IngredientAmount, Purchase,
                     Recipe, Tag)


class IngredientAmountInLine(admin.TabularInline):
    model = IngredientAmount


class IngredientAdmin(admin.ModelAdmin):
    list_display = ("pk", "name",)
    search_fields = ("name",)


class IngredientAmountAdmin(admin.ModelAdmin):
    list_display = ("pk", "recipe", "ingredient", "amount",)  
    search_fields = ("recipe", "ingredient",)

    class Meta: 
        ordering = ("pk",)


class RecipeAdmin(admin.ModelAdmin):
    prepopulated_fields = {"slug": ("title",)}
    inlines = (IngredientAmountInLine, )
    list_display = ("pk", "author", "title")  
    search_fields = ("title",)  
    list_filter = ("title",)  
    empty_value_display = "-пусто-"
    autocomplete_fields = ("ingredients",)


class TagAdmin(admin.ModelAdmin):
    list_display = ("pk", "display_name",)    


class FollowAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "author")  
    search_fields = ("user",)  
    list_filter = ("user",)  
    empty_value_display = "-пусто-" 


class FavouriteAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")  
    search_fields = ("recipe",)  
    list_filter = ("recipe",)  
    empty_value_display = "-пусто-" 


class PurchaseAdmin(admin.ModelAdmin):
    list_display = ("pk", "user", "recipe")  
    search_fields = ("recipe",)  
    list_filter = ("recipe",)  
    empty_value_display = "-пусто-"


admin.site.register(Ingredient, IngredientAdmin)
admin.site.register(IngredientAmount, IngredientAmountAdmin)
admin.site.register(Recipe, RecipeAdmin)
admin.site.register(Tag, TagAdmin)
admin.site.register(Follow, FollowAdmin)
admin.site.register(Favourite, FavouriteAdmin)
admin.site.register(Purchase, PurchaseAdmin)
