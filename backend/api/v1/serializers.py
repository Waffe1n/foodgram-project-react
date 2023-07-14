import base64

from django.core.files.base import ContentFile
from django.db import transaction
from djoser.serializers import UserSerializer
from rest_framework import serializers
from rest_framework.validators import UniqueTogetherValidator, ValidationError

from recipes.models import (Cart, FavoriteRecipe, Follow, Ingredient, Recipe,
                            RecipeIngredient, Tag)
from users.models import CustomUser


class CreateUserSerializer(UserSerializer):
    '''Serializer to work with user creation requests.'''
    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'password'
        )

    def create(self, validated_data):
        '''Custom creation to properly hash user password'''
        password = validated_data.pop('password')
        user = super().create(validated_data)
        user.set_password(password)
        user.save()
        return user


class ShowUserSerializer(UserSerializer):
    '''Serializer to show user info.'''
    is_subscribed = serializers.SerializerMethodField()

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed'
        )

    def get_is_subscribed(self, following):
        '''Get subscriptions info in api response.'''
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.follower.filter(
                following=following
            ).exists()
        )


class Base64ImageField(serializers.ImageField):
    '''Decode image to base64 and save to static.'''
    def to_internal_value(self, data):
        if isinstance(data, str) and data.startswith('data:image'):
            format, imgstr = data.split(';base64,')
            ext = format.split('/')[-1]
            data = ContentFile(base64.b64decode(imgstr), name='temp.' + ext)

        return super().to_internal_value(data)


class IngredientSerializer(serializers.ModelSerializer):
    '''Base ingredient info serializer'''

    class Meta:
        model = Ingredient
        fields = ('id', 'name', 'measurement_unit')
        read_only_fields = ('id', 'name', 'measurement_unit')


class IngredientsInRecipeSerializer(serializers.ModelSerializer):
    '''Serializer used to get additional ingredient info in recipes.'''
    name = serializers.CharField(source='ingredient.name')
    id = serializers.PrimaryKeyRelatedField(
        source='ingredient.id',
        read_only=True,
    )
    measurement_unit = serializers.CharField(
        source='ingredient.measurement_unit'
    )
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'name', 'measurement_unit', 'amount')
        read_only_fields = ('id', 'name', 'measurement_unit', 'amount')


class IngredientAmountSerializer(serializers.ModelSerializer):
    '''Serializer to tie ingredient id with it's amount in short form.'''
    id = serializers.PrimaryKeyRelatedField(queryset=Ingredient.objects.all())
    amount = serializers.IntegerField()

    class Meta:
        model = RecipeIngredient
        fields = ('id', 'amount')


class TagSerializer(serializers.ModelSerializer):
    '''Base tag model serializer.'''

    class Meta:
        model = Tag
        fields = ('id', 'name', 'color', 'slug',)
        read_only_fields = ('id', 'name', 'color', 'slug')


class ShowRecipeSerializer(serializers.ModelSerializer):
    '''Shows RecipeSerializer with additional fields'''
    tags = TagSerializer(read_only=True, many=True,)
    author = ShowUserSerializer(read_only=True)
    ingredients = IngredientsInRecipeSerializer(
        read_only=True,
        many=True,
        source='recipe_ingredient')
    image = Base64ImageField(required=False)
    is_favorited = serializers.SerializerMethodField()
    is_in_shopping_cart = serializers.SerializerMethodField()

    class Meta:
        model = Recipe
        fields = (
            'id',
            'tags',
            'author',
            'ingredients',
            'is_favorited',
            'is_in_shopping_cart',
            'name',
            'image',
            'text',
            'cooking_time'
        )

    def get_is_in_shopping_cart(self, cart):
        '''Shows 'Cart' status of recipe.'''
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.cart.filter(
                recipe=cart
            ).exists()
        )

    def get_is_favorited(self, favorited):
        '''Shows 'Favorites' status of recipe.'''
        user = self.context.get('request').user
        return (
            user.is_authenticated
            and user.favorites.filter(
                recipe=favorited
            ).exists()
        )


class ShortRecipeSerializer(serializers.ModelSerializer):
    '''Serializer used in Cart/Favorite endpoints.Gives a short recipe info.'''

    class Meta:
        model = Recipe
        fields = ('id', 'name', 'image', 'cooking_time')
        read_only_fields = ('id', 'name', 'image', 'cooking_time')


class RecipeSerializer(serializers.ModelSerializer):
    '''Base internal data recipe serializer.'''
    tags = serializers.PrimaryKeyRelatedField(
        queryset=Tag.objects.all(),
        many=True
    )
    ingredients = IngredientAmountSerializer(many=True)
    image = Base64ImageField()

    class Meta:
        model = Recipe
        fields = (
            'ingredients',
            'name',
            'text',
            'tags',
            'cooking_time',
            'image'
        )
        read_only_fields = (
            'id',
            'author',
            'is_favorited',
            'is_in_shopping_cart',
        )

    def set_ingredients(self, instance, ingredients):
        '''Set recipe's ingredients'''
        recipes_ingredients = []
        for ingredient in ingredients:
            iter_ingredient = ingredient.get('id')
            amount = ingredient.get('amount')
            recipes_ingredients.append(
                RecipeIngredient(
                    recipe=instance,
                    ingredient=iter_ingredient,
                    amount=amount
                )
            )
        RecipeIngredient.objects.bulk_create(recipes_ingredients)

    @transaction.atomic
    def create(self, validated_data):
        user = self.context.get('request').user
        tags = validated_data.pop('tags')
        ingredients = validated_data.pop('ingredients')
        instance = Recipe.objects.create(
            author=user, **validated_data)
        instance.tags.set(tags)
        self.set_ingredients(instance, ingredients)
        return instance

    @transaction.atomic
    def update(self, instance, validated_data):
        ingredients = validated_data.pop('ingredients')
        tags = validated_data.pop('tags')
        instance.tags.clear()
        instance.tags.set(tags)
        RecipeIngredient.objects.filter(recipe=instance).delete()

        super().update(instance, validated_data)
        self.set_ingredients(instance, ingredients)
        instance.save()
        return instance

    def to_representation(self, instance):
        return ShowRecipeSerializer(
            instance,
            context={'request': self.context.get('request')}
        ).data

    def validate(self, data):
        ingredient_data = []
        for ingredient in data.get('ingredients'):
            if ingredient.get('amount') < 1:
                raise serializers.ValidationError(
                    'Количество не может быть меньше 1.'
                )
            ingredient_data.append(ingredient.get('id'))
        if len(set(ingredient_data)) < len(ingredient_data):
            raise serializers.ValidationError(
                'Нельзя добавить ингредиент дважды.')
        if data.get('cooking_time') < 1:
            return serializers.ValidationError(
                'Введено некорректное время приготовления.'
            )
        return data


class CartSerializer(serializers.ModelSerializer):
    '''Serializer to perform operations with shopping cart items.'''
    class Meta:
        model = Cart
        fields = ('user', 'recipe')
        validators = [UniqueTogetherValidator(
            queryset=Cart.objects.all(),
            fields=('user', 'recipe'),
            message='Вы уже добавили этот рецепт в корзину.'), ]

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class FavoriteRecipeSerializer(serializers.ModelSerializer):
    '''Serializer for favorites endpoint data serialization.'''
    class Meta:
        model = FavoriteRecipe
        fields = ('user', 'recipe')
        validators = [UniqueTogetherValidator(
            queryset=FavoriteRecipe.objects.all(),
            fields=('user', 'recipe'),
            message='Вы уже добавили рецепт в избранное.'
        ), ]

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.recipe,
            context={'request': self.context.get('request')}
        ).data


class UserRecipesSerializer(serializers.ModelSerializer):
    '''Serializes complete user's info with his recipes alltogether.'''
    recipes = serializers.SerializerMethodField()
    is_subscribed = serializers.BooleanField(read_only=True)

    class Meta:
        model = CustomUser
        fields = (
            'email',
            'id',
            'username',
            'first_name',
            'last_name',
            'is_subscribed',
            'recipes'
        )

    def get_recipes(self, obj):
        '''Get user's recipes with query-based recipe limit.'''
        request = self.context.get('request')
        recipes = obj.author.all()
        if request:
            recipes_limit = request.query_params.get('recipes_limit')
        if recipes_limit:
            recipes = recipes[:int(recipes_limit)]
        return ShortRecipeSerializer(
            recipes, many=True,
            context={'request': request}
        ).data


class FollowSerializer(serializers.ModelSerializer):
    '''Serialize follow endpoints data.'''
    class Meta:
        model = Follow
        fields = ('user', 'following')
        validators = [UniqueTogetherValidator(
            queryset=Follow.objects.all(),
            fields=('user', 'following',),
            message='Вы уже подписаны на этого автора!'
        ), ]

    def validate(self, data):
        request = self.context['request']
        if request.user == data.get('following'):
            return ValidationError(
                'Нельзя подписаться на самого себя.'
            )
        return super().validate(data)

    def to_representation(self, instance):
        return ShortRecipeSerializer(
            instance.following,
            context={'request': self.context.get('request')}
        ).data
