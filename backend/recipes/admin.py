from django import forms
from django.conf import settings
from django.contrib.admin import ModelAdmin, TabularInline, register
from django.core.exceptions import ValidationError

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


class RecipeForm(forms.ModelForm):
    model = Recipe
    fields = [
        'name',
        'author',
        'text',
        'image',
        'ingredients',
        'tags',
        'cooking_time'
    ]

    def clean(self):
        ingredients = self.cleaned_data.get('ingredients')
        if len(ingredients) < 1:
            raise ValidationError('Добавьте хотя бы один ингредиент.')
        return self.cleaned_data


@register(Recipe)
class RecipeAdmin(ModelAdmin):
    form = RecipeForm
    list_display = ('pk', 'name', 'author', 'favorites_amount', 'ingredient')
    list_filter = ('name', 'author', 'tags')
    empty_value_display = settings.EMPTY_VALUE
    inlines = [RecipeIngredientInline, ]

    def favorites_amount(self, obj):
        return obj.favorites.count()

    def ingredient(self, obj):
        return (
            [recipe_ingredient.ingredient for
             recipe_ingredient in
             obj.recipe_ingredient.all()]
        )


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
