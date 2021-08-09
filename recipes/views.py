import io

from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.http import FileResponse
from django.shortcuts import get_object_or_404, redirect, render
from reportlab.pdfbase import pdfmetrics
from reportlab.pdfbase.ttfonts import TTFont
from reportlab.pdfgen import canvas

from .forms import RecipeForm
from .models import Follow, IngredientAmount, Purchase, Recipe, Tag, User
from .utils import total_ingredients


def filtered_by_tags(request, recipes):
    """ Функция для фильтрации рецептов по тегам """
    get_tags = request.GET.getlist("tags")
    if get_tags:
        recipes = recipes.filter(tags__title__in=get_tags).distinct()
    return recipes


def index(request):
    """ View-функция для отображения главной страницы """
    recipes = Recipe.objects.all().order_by("-pub_date")
    recipes = filtered_by_tags(request, recipes)
    tags = Tag.objects.all()
    paginator = Paginator(recipes, 6)
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page, 
        "paginator": paginator, 
        "tags": tags,
    }
    return render(request, "index.html", context)


def view_recipe(request, recipe_id):
    """ View-функция для отображения страницы рецепта """
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id) 
    author = recipe.author
    context = {
        "recipe": recipe,
    }
    if user.is_authenticated: 
        following = Follow.objects.filter(user=user, author=author) 
        context.update({"following": following})
    return render(request, "recipe.html", context)          


@login_required
def view_profile(request, username):
    """ View-функция для отображения профиля пользователя """
    recipes = Recipe.objects.filter(
        author__username=username).order_by("-pub_date")
    recipes = filtered_by_tags(request, recipes)
    tags = Tag.objects.all()
    user = request.user 
    author = get_object_or_404(User, username=username) 
    paginator = Paginator(recipes, 6) 
    page_number = request.GET.get("page") 
    page = paginator.get_page(page_number)
    context = {
        "author": author, 
        "page": page, 
        "paginator": paginator, 
        "tags": tags,
    } 
    if user.is_authenticated: 
        following = Follow.objects.filter(author=author, user=user) 
        context.update({"following": following})         
    return render(request, "profile.html", context)


@login_required
def new_recipe(request):
    """ View-функция для создания рецепта """
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    context = {
        "form": form,
        "new": "new",
    }
    if form.is_valid(): 
        form.save(request) 
        return redirect("index")
    return render(request, "create_edit_recipe.html", context)


@login_required
def edit_recipe(request, recipe_id):
    """ View-функция для редактирования рецепта """
    user = request.user
    recipe = get_object_or_404(Recipe, id=recipe_id) 
    author = recipe.author
    if author != user: 
        return redirect("index")
    form = RecipeForm(request.POST or None, 
                      instance=recipe, files=request.FILES or None)
    context = {
        "form": form,
        "edit": "edit",
    }
    if form.is_valid():
        IngredientAmount.objects.filter(recipe=recipe).delete()
        recipe = form.save(request)
        return redirect("view_recipe", recipe_id)
    return render(request, "create_edit_recipe.html", context)

 
@login_required
def delete_recipe(request, recipe_id):
    """ View-функция для удаления рецепта """
    recipe = get_object_or_404(Recipe, id=recipe_id) 
    recipe.delete()
    return redirect("profile", username=request.user.username)  


@login_required
def subscriptions(request):
    """ View-функция для отображения подписок пользователя """
    authors = User.objects.filter(
        following__user=request.user).order_by("-id")
    paginator = Paginator(authors, 3) 
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page, 
        "paginator": paginator
    }
    return render(request, "my_follow.html", context)  


@login_required
def favourites(request):
    """ View-функция для отображения избранных рецептов автора """
    recipes = Recipe.objects.filter(
        favoured_by__user=request.user).order_by("-pub_date")
    recipes = filtered_by_tags(request, recipes)
    tags = Tag.objects.all()
    paginator = Paginator(recipes, 3) 
    page_number = request.GET.get("page")
    page = paginator.get_page(page_number)
    context = {
        "page": page, 
        "paginator": paginator, 
        "tags": tags
    }
    return render(request, "favorite.html", context)


@login_required
def purchases(request):
    """ View-функция для отображения покупок """
    recipes = Recipe.objects.filter(
        purchased_recipe__user=request.user).order_by("-pub_date")
    context = {
        "recipes": recipes,
    }
    return render(request, "shop_list.html", context)


def delete_purchase(request, recipe_id):
    """ View-функция для удаления рецепта из покупок """
    recipe = get_object_or_404(Purchase, recipe__id=recipe_id,
                               user=request.user)
    recipe.delete()
    return redirect("purchases")


def print_pdf(request):
    """ View-функция для распечатки рецепта """
    title = "Список покупок"
    buffer = io.BytesIO()
    pdf = canvas.Canvas(buffer)
    pdf.setLineWidth(170)
    pdfmetrics.registerFont(TTFont("TNR", "times.ttf"))
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
    return FileResponse(buffer, as_attachment=True, filename="purchases.pdf")
