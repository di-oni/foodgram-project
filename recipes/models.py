from django.contrib.auth import get_user_model
from django.core.validators import MinValueValidator
from django.db import models

from decimal import Decimal


User = get_user_model()


class Ingredient(models.Model):
    """ Модель объекта "Ингредиент" """
    name = models.CharField("Наименование", max_length=250)
    units = models.CharField("Ед. измерения", max_length=50)

    class Meta: 
        ordering = ("name",)
        verbose_name = "Ингредиент"
        verbose_name_plural = "Ингредиенты" 

    def __str__(self):
        return self.name      


class Tag(models.Model):
    """ Модель объекта "Тэг" """
    title = models.CharField("Имя тега", max_length=50, db_index=True)
    display_name = models.CharField("Имя тега", max_length=50)
    colour = models.CharField("Цвет", max_length=50)

    class Meta:
        verbose_name = "Тег"
        verbose_name_plural = "Теги"

    def __str__(self):
        return self.title


class Recipe(models.Model):
    """ Модель объекта "Рецепт" """
    author = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="recipes",
        verbose_name="Автор рецепта",
    )
    title = models.CharField("Название блюда", max_length=100)
    photo = models.ImageField(
        "Изображение",
        upload_to="recipes/",
    )
    description = models.TextField("Как готовить",)
    ingredients = models.ManyToManyField(
        Ingredient,
        through="IngredientAmount",
        related_name="recipes",
        verbose_name="Ингредиенты",
    )
    tags = models.ManyToManyField(
        Tag,
        related_name="tags",
        verbose_name="Теги",
    )
    cooking_time = models.PositiveSmallIntegerField(
        "Время приготовления",
    )
    slug = models.SlugField(
        blank=True,
    )
    pub_date = models.DateTimeField("date published", auto_now_add=True)

    class Meta:
        verbose_name = "Рецепт"
        verbose_name_plural = "Рецепты"

    def __str__(self): 
        return self.title


class IngredientAmount(models.Model):
    """ Промежуточная модель объекта "Количество ингредиента", 
        связывающая модели рецепта и ингредиента """
    ingredient = models.ForeignKey(
        Ingredient,
        on_delete=models.CASCADE,
        verbose_name="Ингредиент",
    )
    recipe = models.ForeignKey(
        Recipe, 
        on_delete=models.CASCADE,
        verbose_name="Рецепт",
    )
    amount = models.DecimalField(
        "Количество",
        max_digits=10,
        decimal_places=1,
        validators=[MinValueValidator(Decimal(0.1))]
    )

    class Meta:
        verbose_name = "Количество ингредиента"
        verbose_name_plural = "Количество ингредиента"

    def __str__(self):
        return f"{self.recipe}: {self.ingredient}, {self.amount}"


class Follow(models.Model): 
    """ Модель объекта "Подписка" """
    user = models.ForeignKey( 
        User, 
        related_name="follower", 
        on_delete=models.CASCADE,
        verbose_name="Подписчик",
    ) 
    author = models.ForeignKey( 
        User, 
        related_name="following", 
        on_delete=models.CASCADE,
        verbose_name="Подписан на", 
    )

    class Meta: 
        verbose_name = "Подписка"
        verbose_name_plural = "Подписки"
        constraints = [
            models.UniqueConstraint(fields=["user", "author"], name="unique_Follow")
        ]
     
    def __str__(self): 
        return f"{self.user} подписался на {self.author}."


class Favourite(models.Model):
    """ Модель объекта "Избранное" """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="favours",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="favoured_by",
        verbose_name="Рецепт",
    )

    class Meta: 
        verbose_name = "Избранное"
        verbose_name_plural = "Избранное"
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"], name="unique_Favourite")
        ]

    def __str__(self): 
        return f"{self.user} добавил {self.recipe} в Избранное."


class Purchase(models.Model):
    """ Модель объекта "Покупка" """
    user = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name="purchases",
        verbose_name="Пользователь",
    )
    recipe = models.ForeignKey(
        Recipe,
        on_delete=models.CASCADE,
        related_name="purchased_recipe",
        verbose_name="Рецепт",
    )

    class Meta: 
        verbose_name = "Покупка"
        verbose_name_plural = "Покупки"
        constraints = [
            models.UniqueConstraint(fields=["user", "recipe"], name="unique_Purchase")
        ]

    def __str__(self): 
        return f"{self.user} добавил {self.recipe} в корзину."
