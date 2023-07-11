from django_filters.rest_framework import FilterSet, filters

from recipes.models import Ingredient, Recipe, Tag


class RecipeFilter(FilterSet):
    """Custom recipe filter by tag, favorite/cart lists presence."""
    tags = filters.ModelMultipleChoiceFilter(
        queryset=Tag.objects.all(),
        field_name='tags__slug',
        to_field_name='slug',
        lookup_expr='exact'
    )
    is_favorited = filters.BooleanFilter(
        method='check_if_favorited'
    )
    is_in_shopping_cart = filters.BooleanFilter(
        method='check_if_in_shopping_cart'
    )

    class Meta:
        model = Recipe
        fields = ('author', 'tags', 'is_favorited', 'is_in_shopping_cart')

    def check_if_favorited(self, queryset, value, data):
        if self.request.user.is_authenticated and value:
            return queryset.filter(favorites__user=self.request.user)

    def check_if_in_shopping_cart(self, queryset, value, data):
        return queryset.filter(cart__user=self.request.user)


class IngredientFilter(FilterSet):
    '''Ingredient filtration by starting expression'''
    name = filters.CharFilter(lookup_expr='istartswith')

    class Meta:
        model = Ingredient
        fields = ('name', )
