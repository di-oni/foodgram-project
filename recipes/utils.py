from recipes.models import IngredientAmount, Tag


def filtered_by_tags(request, recipes):
    """ Функция для фильтрации рецептов по тегам """
    get_tags = request.GET.getlist("tags")
    if get_tags:
        recipes = recipes.filter(tags__title__in=get_tags).distinct()
    return recipes


def get_ingredients(request):
    """ Функция для получения ингредиентов из запроса """
    ingredients = {}
    for key in request:
        if key.startswith("nameIngredient"):
            count = key.split("_")[1]
            value = request[f"valueIngredient_{count}"]
            ingredients[request[key]] = value
    return ingredients


def get_tags(request):
    """ Функция для получения тэгов из запроса """
    tags = []
    data = request.POST
    tag_list = [item.title for item in Tag.objects.all()]
    for item in tag_list:
        if item in data:
            tags.append(item)
    return tags


def total_ingredients(user_id):
    """ Функция для получения ингредиетов для рецептов в списке """   
    cart = {}
    cart_as_text = []
    ingredients = IngredientAmount.objects.filter(
        recipe__purchased_recipe__user=user_id)
    for ingredient in ingredients:
        id =  ingredient.ingredient.pk 
        name = ingredient.ingredient.name
        amount = ingredient.amount
        units = ingredient.ingredient.units
        if id in cart:
            cart_name, cart_amount, cart_units = cart[id]
            cart_amount += amount
            cart[id] = (cart_name, cart_amount, cart_units)
        else:
            cart[id] = name, amount, units
    for name, amount, units in cart.values():
        line = f"{name}: {amount} {units}"
        cart_as_text.append(line)
    return cart_as_text
