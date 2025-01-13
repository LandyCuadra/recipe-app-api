"""URL mapping for the recipe app"""

from django.urls import include, path
from rest_framework.routers import DefaultRouter
from recipe import views

router = DefaultRouter()
router.register('recipes', views.RecipeViewSet)
router.register('tag', views.TagViewSet)
router.register('ingredient', views.IngredientViewSet)

app_name = 'recipe'

urlpatterns = [
    path('', include(router.urls)),
]
