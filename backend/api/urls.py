from django.urls import include, path
from rest_framework import routers

from api.v1.views import (FollowListApiView, FollowUserView, IngredientViewSet,
                          RecipeViewSet, TagViewSet)

router_v1 = routers.DefaultRouter()

router_v1.register(r'ingredients', IngredientViewSet, basename='ingredients')
router_v1.register(r'tags', TagViewSet, basename='tags')
router_v1.register(r'recipes', RecipeViewSet, basename='recipes')


urlpatterns = [
    path('', include(router_v1.urls)),
    path('users/<int:user_id>/subscribe/', FollowUserView.as_view()),
    path('users/subscriptions/', FollowListApiView.as_view()),

    path('', include('djoser.urls')),
    path('auth/', include('djoser.urls.authtoken'))
]
