from django import template

from recipes.models import Favourite, Follow, Purchase, Tag


register = template.Library()


@register.simple_tag 
def current_url(request):
    if request.resolver_match:
        current_url = request.resolver_match.view_name
        return current_url


@register.filter 
def decline(word, amount):
    amount_by_ten = amount % 10
    amount_by_hundred = amount % 100
    if amount_by_ten == 1 and amount_by_hundred != 11:
        return word
    if amount_by_ten in [2, 3, 4]:
        if amount_by_hundred not in [11, 12, 13, 14]:
            return word + "а"
        else:
            return word + "ов"
    elif amount_by_ten in [5, 6, 7, 8, 9, 0]:
        return word + "ов"


@register.filter 
def request_get(request, tag):
    tags = request.GET.getlist("tags")
    if tag in tags:
        tags = [item for item in tags if item != tag]
    else:
        tags.append(tag)
    new = request.GET.copy()
    new.setlist("tags", tags)
    return new.urlencode()


@register.filter 
def get_tags(request):
    tags = request.GET.getlist("tags")
    if len(tags) == 3:
        tags.clear()
    return tags


@register.simple_tag 
def is_favourite(recipe, user):
    return Favourite.objects.filter(user=user, recipe=recipe).exists()


@register.simple_tag 
def purchases_amount(user):
    return Purchase.objects.filter(user=user).count()


@register.simple_tag
def is_purchased(recipe, user):
    return Purchase.objects.filter(user=user, recipe=recipe).exists()


@register.simple_tag
def is_followed(author, user):
    return Follow.objects.filter(user=user, author=author).exists()  


@register.filter
def startswith(text, starts):
    if isinstance(text, str):
        return text.startswith(starts)
    return False


@register.filter
def tags_for_page(tags):

    tags = "".join([f"&tags={tag}" for tag in tags])
    return tags
