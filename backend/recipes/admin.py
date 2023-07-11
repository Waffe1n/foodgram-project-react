from django.conf import settings
from django.contrib.admin import ModelAdmin, TabularInline, register

from .models import (Cart, FavoriteRecipe, Ingredient, Recipe,
                     RecipeIngredient, Tag)


@register(Ingredient)
class IngredientAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'measurement_unit')
    search_fields = ('name',)
    list_filter = ('name',)
    empty_value_display = settings.EMPTY_VALUE


@register(Tag)
class TagAdmin(ModelAdmin):
    list_display = ('pk', 'name', 'color', 'slug')
    search_fields = ('name', 'color', 'slug')
    list_filter = ('name', 'color', 'slug')
    empty_value_display = settings.EMPTY_VALUE


class RecipeIngredientInline(TabularInline):
    model = RecipeIngredient


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    list_display = (
        'pk',
        'name',
        'author',
        'favorites_amount'
    )
    list_filter = ('name', 'author', 'tags')
    empty_value_display = settings.EMPTY_VALUE
    inlines = [RecipeIngredientInline, ]

    def favorites_amount(self, obj):
        return obj.favorites.count()


@register(RecipeIngredient)
class RecipeIngredientAdmin(ModelAdmin):
    list_display = ('pk', 'recipe', 'ingredient', 'amount')
    empty_value_display = settings.EMPTY_VALUE


@register(FavoriteRecipe)
class FavoriteAdmin(ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = settings.EMPTY_VALUE


@register(Cart)
class CartAdmin(ModelAdmin):
    list_display = ('pk', 'user', 'recipe')
    search_fields = ('user', 'recipe')
    empty_value_display = settings.EMPTY_VALUE
