from django import forms

from .models import Ingredient, Recipe, Tag


class IngredientForm(forms.ModelForm):
    """ Форма для объектов модели "Ингредиент" """
    class Meta: 
        model = Ingredient 
        fields = ('name', 'units') 
        labels = { 
            'name': "Название", 
            'units': "Единицы измерения",
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
            'id', 
            "title", 
            "photo", 
            "description", 
            'tags', 
            "cooking_time",
        ) 
        labels = { 
            "title": "Название", 
            "photo": "Загрузите изображение",
            "description": "Описание",
            "cooking_time": "Время приготовления",
        } 
    
