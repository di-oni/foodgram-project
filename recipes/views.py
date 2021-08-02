import io

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse
from django.http.response import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from django.views.decorators.cache import cache_page
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .forms import RecipeForm
from .models import (Follow, Ingredient, IngredientAmount, Purchase, Recipe,
                     Tag, User)
from .utils import get_ingredients, total_ingredients


def index(request):
    """ View-функция для отображения главной страницы """
    get_tags = request.GET.getlist('tags')
    if get_tags:
        recipes = Recipe.objects.filter(
            tags__title__in=get_tags).order_by('-pub_date')
    else:
        recipes = Recipe.objects.all().order_by('-pub_date')
    tags = Tag.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request, 
        'index.html', 
        {
            'page': page, 
            'paginator': paginator, 
            'tags': tags
        }
    )


def view_recipe(request, recipe_id):
    """ View-функция для отображения страницы рецепта """
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id) 
    author = recipe.author
    if user.is_authenticated: 
        following = Follow.objects.filter(user=user, author=author) 
        return render(request, 'recipe.html', {"recipe": recipe, 
                                               "following": following,})
    return render(request, 'recipe.html', {"recipe": recipe,})          


def view_profile(request, username):
    """ View-функция для отображения профиля пользователя """
    get_tags = request.GET.getlist('tags')
    recipes = Recipe.objects.filter(
        author__username=username).order_by('-pub_date')
    if get_tags:
        recipes = recipes.filter(
            tags__title__in=get_tags).order_by('-pub_date')
    tags = Tag.objects.all()
    user = request.user 
    author = get_object_or_404(User, username=username) 
    paginator = Paginator(recipes, 5) 
    page_number = request.GET.get('page') 
    page = paginator.get_page(page_number) 
    if user.is_authenticated: 
        follow = Follow.objects.filter(user=user, author=author).exists() 
        if follow: 
            following = Follow.objects.get(author=author, user=user) 
            return render( 
                request,  
                'profile.html',  
                { 
                    "author": author,  
                    "page": page,  
                    "paginator": paginator,  
                    "following": following,
                    "tags": tags,
                } 
            ) 
        return render( 
            request,  
            'profile.html',  
            {
                "author": author, 
                "page": page, 
                "paginator": paginator, 
                "tags": tags,
            }
        )         
    return render( 
            request,  
            'profile.html',  
            {
                "author": author, 
                "page": page, 
                "paginator": paginator, 
                "tags": tags,
            }
        )


@login_required
def new_recipe(request):
    """ View-функция для создания рецепта """
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    ingredients = get_ingredients(request)
    if form.is_valid(): 
        recipe = form.save(commit=False) 
        recipe.author = request.user
        recipe.save()  
        items = []
        for name, amount in ingredients.items():
            ingredient = get_object_or_404(Ingredient, name=name)
            items.append(IngredientAmount(recipe=recipe, 
                                          ingredient=ingredient, 
                                          amount=int(amount)))
        IngredientAmount.objects.bulk_create(items)
        form.save_m2m()
        return redirect('index') 
    return render( 
        request,  
        "new_recipe.html",  
        {"form": form})


@login_required
def edit_recipe(request, recipe_id):
    """ View-функция для редактирования рецепта """
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id) 
    author = recipe.author
    if author != user: 
        return redirect('index')
    form = RecipeForm(request.POST or None, 
                      instance=recipe, files=request.FILES or None)
    ingredients = get_ingredients(request)
    if form.is_valid(): 
        recipe = form.save(commit=False) 
        recipe.author = request.user
        recipe.save() 
        recipe.ingredientamount_set.all().delete()
        items = []
        for name, amount in ingredients.items():
            ingredient = get_object_or_404(Ingredient, name=name)
            amount = int(amount.partition(',')[0])
            items.append(IngredientAmount(recipe=recipe, 
                                          ingredient=ingredient, 
                                          amount=amount))
        IngredientAmount.objects.bulk_create(items)
        form.save_m2m()
        return redirect('view_recipe', recipe_id) 
    return render( 
        request,  
        "edit_recipe.html",  
        {"form": form}
    )   

 
@login_required
def delete_recipe(request, recipe_id):
    """ View-функция для удаления рецепта """
    recipe = get_object_or_404(Recipe, id=recipe_id) 
    recipe.delete()
    return redirect('view_profile', username=request.user.username)  


def subscriptions(request):
    """ View-функция для отображения подписок пользователя """
    authors = User.objects.filter(
        following__user=request.user).order_by('-id')
    paginator = Paginator(authors, 3) 
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number) 
    return render(
        request, 
        'my_follow.html', 
        {
            'page': page, 
            'paginator': paginator
        }
    )  


def favourites(request):
    """ View-функция для отображения избранных рецептов автора """
    get_tags = request.GET.getlist('tags')
    recipes = Recipe.objects.filter(
        favoured_by__user=request.user).order_by('-pub_date')
    if get_tags:
        recipes = recipes.filter(tags__title__in=get_tags).order_by('-id')
    tags = Tag.objects.all()
    paginator = Paginator(recipes, 3) 
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number) 
    return render(
        request, 
        'favorite.html', 
        {
            'page': page, 
            'paginator': paginator, 
            'tags': tags
        }
    )


def purchases(request):
    """ View-функция для отображения покупок """
    recipes = Recipe.objects.filter(
        purchased_recipe__user=request.user).order_by('-pub_date')
    return render(request, 'shop_list.html', {'recipes': recipes})


def delete_purchase(request, recipe_id):
    """ View-функция для удаления рецепта из покупок """
    recipe = get_object_or_404(Purchase, recipe__id=recipe_id,
                               user=request.user)
    recipe.delete()
    return redirect('purchases')


def print_pdf(request):
    """ View-функция для распечатки рецепта """
    title = 'Список покупок'
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setLineWidth(170)
    pdfmetrics.registerFont(TTFont('TNR', 'times.ttf'))
    pdf.setFont("TNR", 28)
    pdf.drawCentredString(300, 700, title)
    pdf.setFont("TNR", 14)
    ingredients = total_ingredients(request.user.id)
    y = 650
    for item in ingredients:
        pdf.drawString(150, y, item)
        y = y - 20
    pdf.showPage()
    pdf.save()
    buffer.seek(0)
    return FileResponse(buffer, as_attachment=True, filename='purchases.pdf')
