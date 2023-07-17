from django.conf import settings
from django.contrib.admin import ModelAdmin, TabularInline, register
from django.forms import models, ValidationError

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


class MinValidatedMixin:
    validate_min = True

    def get_formset(self, *args, **kwargs):
        return super().get_formset(
            validate_min=self.validate_min, *args, **kwargs
        )


class RecipeIngredientFormset(models.BaseInlineFormSet):
    def is_valid(self):
        return (super(RecipeIngredientFormset, self).is_valid()
                and not any([bool(exc) for exc in self.errors]))

    def clean(self):
        count = 0
        for form in self.forms:
            try:
                if form.cleaned_data:
                    count += 1
            except AttributeError:
                # avoid raising AttributeError for empty cleaned_data
                pass
        if count < 1:
            raise ValidationError()


class RecipeIngredientInline(MinValidatedMixin, TabularInline):
    formset = RecipeIngredientFormset
    model = RecipeIngredient
    validate_min = True
    min_num = 1
    extra = 2


@register(Recipe)
class RecipeAdmin(ModelAdmin):
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
