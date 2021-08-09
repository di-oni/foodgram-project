from decimal import Decimal

from django import forms
from django.shortcuts import get_object_or_404

from .models import Ingredient, IngredientAmount, Recipe, Tag
from .utils import get_ingredients


class IngredientForm(forms.ModelForm):
    """ Форма для объектов модели "Ингредиент" """
    class Meta: 
        model = Ingredient 
        fields = ("name", "units") 
        labels = { 
            "name": "Название", 
            "units": "Единицы измерения",
        } 


class RecipeForm(forms.ModelForm): 
    """ Форма для объектов модели "Рецепт" """
    tags = forms.ModelMultipleChoiceField(
        queryset=Tag.objects.all(),
        widget=forms.CheckboxSelectMultiple(),
    )
    class Meta: 
        model = Recipe 
        fields = (
            "id", 
            "title", 
            "photo", 
            "description", 
            "tags", 
            "cooking_time",
        ) 
        labels = { 
            "title": "Название", 
            "photo": "Загрузите изображение",
            "description": "Описание",
            "cooking_time": "Время приготовления",
        } 
    
    def save(self, request, commit=True):
        instance = super().save(commit=False)
        instance.author = request.user 
        instance.save()
        ingredients = get_ingredients(request)
        items = []
        for name, amount in ingredients.items():
            ingredient = get_object_or_404(Ingredient, name=name)
            amount = Decimal(amount.replace(",", "."))
            items.append(IngredientAmount(recipe=instance, 
                                          ingredient=ingredient, 
                                          amount=amount))
        IngredientAmount.objects.bulk_create(items)
        self.save_m2m()
        return instance    
