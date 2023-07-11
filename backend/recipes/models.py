from django.core.validators import MinValueValidator
from django.db import models

from users.models import CustomUser


class Tag(models.Model):
    '''Tags model.'''
    name = models.CharField(unique=True, max_length=200,
                            verbose_name='Название тега',)
    color = models.CharField(unique=True,
                             verbose_name='Цвет', max_length=7)
    slug = models.SlugField(unique=True,
                            verbose_name='Слаг', max_length=200)

    def __str(self):
        return self.name


class Ingredient(models.Model):
    '''Base ingredient model.'''
    name = models.CharField(verbose_name='Название ингредиента',
                            max_length=200)
    measurement_unit = models.CharField(verbose_name='Единица измерения',
                                        max_length=200)

    def __str__(self):
        return self.name


class Recipe(models.Model):
    '''Base recipe model.'''
    name = models.CharField(max_length=200,
                            verbose_name='Название блюда',)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                               related_name='author',
                               verbose_name='Автор',)
    text = models.TextField(verbose_name='Текст рецепта')
    ingredients = models.ManyToManyField(
        Ingredient, through='RecipeIngredient',
        through_fields=('recipe', 'ingredient'),
        verbose_name='Ингредиенты')
    image = models.ImageField(upload_to='static/recipes/',
                              blank=True, null=True,
                              verbose_name='Изображение')
    tags = models.ManyToManyField(Tag, related_name='tags',
                                  verbose_name='Теги')
    cooking_time = models.PositiveSmallIntegerField(
        verbose_name='Время приготовления',
        validators=[MinValueValidator(1), ])

    pub_date = models.DateTimeField(auto_now=True,
                                    verbose_name='Дата публикации')

    class Meta:
        ordering = ['-pub_date', ]

    def __str__(self):
        return self.name


class RecipeIngredient(models.Model):
    '''Many-to-many recipe-ingredient relation model.'''
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='recipe_ingredient',
                               verbose_name='Рецепт')
    ingredient = models.ForeignKey(Ingredient, on_delete=models.CASCADE,
                                   related_name='recipe_ingredient',
                                   verbose_name='ингридиент')
    amount = models.IntegerField(verbose_name='количество')


class FavoriteRecipe(models.Model):
    '''Many-to-many user's favorite recipes model.'''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             related_name='favorites',
                             verbose_name='Пользователь')
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='favorites',
                               verbose_name='рецепт')

    class Meta:
        constraints = [models.constraints.UniqueConstraint(
            fields=('user', 'recipe'), name='unique_favorite'), ]


class Follow(models.Model):
    '''Many-to-many user's subscriptions model.'''
    user = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='follower',
        verbose_name='Подписчик',
    )
    following = models.ForeignKey(
        CustomUser, on_delete=models.CASCADE,
        related_name='subscriptions',
        verbose_name='Подписка',
    )

    class Meta:
        constraints = [models.constraints.UniqueConstraint(
            fields=('user', 'following'), name='unique_follow'), ]


class Cart(models.Model):
    '''Ingredient shopping cart model.'''
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE,
                             verbose_name='пользователь',
                             related_name='cart',)
    recipe = models.ForeignKey(Recipe, on_delete=models.CASCADE,
                               related_name='cart',
                               verbose_name='рецепты')

    class Meta:
        constraints = [models.constraints.UniqueConstraint(
            fields=('user', 'recipe'), name='unique_cart_recipe',
        ), ]
