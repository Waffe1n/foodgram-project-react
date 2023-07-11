from django.db.models import Count
from django.shortcuts import get_object_or_404
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, views, viewsets
from rest_framework.decorators import action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response

from recipes.models import Cart, FavoriteRecipe, Ingredient, Recipe, Tag
from users.models import CustomUser

from .filters import IngredientFilter, RecipeFilter
from .paginators import LimitPageNumberPagination
from .permissions import IsAuthor
from .serializers import (CartSerializer, FavoriteRecipeSerializer, Follow,
                          FollowSerializer, IngredientSerializer,
                          RecipeSerializer, ShowRecipeSerializer,
                          TagSerializer, UserRecipesSerializer)
from .services import create_pdf


class CreateDeleteObjMixin:
    '''Mixin for adding sample recipe-related create/delete methods.'''

    def create_obj(self, instance, serializer, request):
        serializer = serializer(
            data={'user': request.user.id, 'recipe': instance.id, },
            context={'request': request})

        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete_obj(self, instance, model, request, error):
        if model.objects.filter(user=request.user, recipe=instance).exists():
            model.objects.filter(user=request.user, recipe=instance).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response({'errors': error, },
                        status=status.HTTP_400_BAD_REQUEST)


class IngredientViewSet(viewsets.ReadOnlyModelViewSet):
    '''Base ingredient list viewset.'''
    queryset = Ingredient.objects.all()
    serializer_class = IngredientSerializer
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = IngredientFilter


class TagViewSet(viewsets.ReadOnlyModelViewSet):
    ''''Base tag list viewset.'''
    queryset = Tag.objects.all()
    serializer_class = TagSerializer


class RecipeViewSet(CreateDeleteObjMixin, viewsets.ModelViewSet):
    '''Base recipe list viewset.'''
    queryset = Recipe.objects.all()
    pagination_class = LimitPageNumberPagination
    filter_backends = [DjangoFilterBackend, ]
    filterset_class = RecipeFilter
    http_method_names = [
        'get',
        'post',
        'patch',
        'delete'
    ]

    def get_permissions(self):
        if self.action == ('list' or 'retrieve'):
            permission_classes = [AllowAny, ]
        elif self.action == 'post':
            permission_classes = [IsAuthenticated, ]
        else:
            permission_classes = [IsAuthor, ]
        return [permission() for permission in permission_classes]

    def get_serializer_class(self):
        if self.action == ('list' or 'retrieve'):
            return ShowRecipeSerializer
        return RecipeSerializer

    @action(detail=True,
            methods=['post'],
            permission_classes=[IsAuthenticated, ])
    def favorite(self, request, pk):
        '''Custom action routing for adding recipe to favorites.'''
        recipe = get_object_or_404(
            Recipe, pk=pk)
        obj = self.create_obj(
            recipe,
            FavoriteRecipeSerializer,
            request)
        return obj

    @favorite.mapping.delete
    def favorite_destroy(self, request, pk):
        '''Delete recipe from favorites list.'''
        error = 'Этого рецепта нет в списке избранных.'
        return self.delete_obj(
            get_object_or_404(Recipe, pk=pk),
            FavoriteRecipe,
            request,
            error
        )

    @action(
        detail=True,
        methods=('post',),
        permission_classes=(IsAuthenticated,)
    )
    def shopping_cart(self, request, pk):
        '''Custom routing for creating cart objects.'''
        return self.create_obj(
            get_object_or_404(Recipe, pk=pk),
            CartSerializer,
            request
        )

    @shopping_cart.mapping.delete
    def shopping_cart_delete(self, request, pk):
        '''Delete recipes cart relational object.'''
        error = 'Этого рецепта нет в списке покупок.'
        return self.delete_obj(
            get_object_or_404(Recipe, pk=pk),
            Cart,
            request,
            error
        )

    @action(detail=False,
            methods=['get'],
            permission_classes=(IsAuthenticated,))
    def download_shopping_cart(self, request):
        '''Download ingredient list from cart's recipes.'''
        return create_pdf(request)


class FollowUserView(views.APIView):
    '''Custom APIView for create/delete operations on follow objects.'''
    permission_classes = [IsAuthenticated, ]

    def post(self, request, user_id):
        following = get_object_or_404(CustomUser, id=user_id)
        serializer = FollowSerializer(
            data={'user': request.user.id,
                  'following': following.id},
            context={'request': request})
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)

    def delete(self, request, user_id):
        following = get_object_or_404(CustomUser, pk=user_id)
        if Follow.objects.filter(
                user=request.user, following=following).exists():
            Follow.objects.get(user=request.user, following=following).delete()
            return Response(status=status.HTTP_204_NO_CONTENT)
        return Response(
            {'error': 'Вы не подписаны на профиль этого пользователя', },
            status=status.HTTP_400_BAD_REQUEST)


class FollowListApiView(generics.ListAPIView):
    '''APIView for getting user's follow objects.'''
    serializer_class = UserRecipesSerializer
    pagination_class = LimitPageNumberPagination
    permission_classes = [IsAuthenticated, ]

    def get_queryset(self):
        qs = CustomUser.objects.filter(
            follower__following__id=self.request.user.id)
        qs.annotate(recipes_count=Count('author'))
        return qs
