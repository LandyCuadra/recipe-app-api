"""Tests for the ingredients API"""
from django.contrib.auth import get_user_model
from django.test import TestCase
from django.urls import reverse
from rest_framework.test import APIClient
from rest_framework import status
from core.models import Ingredient
from recipe.serializers import IngredientSerializer

INGREDIENTS_URL = reverse('recipe:ingredient-list')


def detail_url(ingredient_id: str):
    return reverse('recipe:ingredient-detail', args=[ingredient_id])


def create_user(email='user@example.com',  password='testpass123'):
    """Create and return user."""
    return get_user_model().objects.create_user(
        email=email,
        password=password,
    )


class PublicIngredientApiTest(TestCase):
    """Test unauthenticated API requests."""

    def setUp(self) -> None:
        self.client = APIClient()

    def test_auth_required(self):
        """Test auth is required for retrieving ingredients."""
        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_401_UNAUTHORIZED)


class PrivateIngredientApiTest(TestCase):
    """Test authenticated API request"""

    def setUp(self) -> None:
        self.client = APIClient()
        self.user = create_user()
        self.client.force_authenticate(self.user)

    def test_retrieve_ingredients(self):
        """Test retrieving a list of ingredients."""
        Ingredient.objects.create(user=self.user, name='Kale')
        Ingredient.objects.create(user=self.user, name='Vanilla')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 2)
        ingredients = Ingredient.objects.all().order_by('-name')
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_ingredient_limited_to_user(self):
        """Test list of ingredients is limited to authenticated user."""
        user2 = create_user(email='user2@example.com')
        Ingredient.objects.create(user=self.user, name='Salt')
        Ingredient.objects.create(user=user2, name='Pepper')

        res = self.client.get(INGREDIENTS_URL)

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        self.assertEqual(len(res.data), 1)
        ingredients = Ingredient.objects.filter(user=self.user)
        serializer = IngredientSerializer(ingredients, many=True)
        self.assertEqual(res.data, serializer.data)

    def test_update_ingredient(self):
        """Test updating an ingredient"""

        ingredient = Ingredient.objects.create(user=self.user, name='Cilantro')

        url = detail_url(ingredient.id)
        payload = {"name": 'Coriander'}
        res = self.client.patch(url, payload, format='json')

        self.assertEqual(res.status_code, status.HTTP_200_OK)
        ingredient.refresh_from_db()
        self.assertEqual(ingredient.name, payload['name'])

    def test_delete_ingredient(self):
        """Test deleting an ingredient"""
        ingredient = Ingredient.objects.create(user=self.user, name='lettuce')
        url = detail_url(ingredient.id)

        self.assertEqual(Ingredient.objects.all().count(), 1)
        res = self.client.delete(url)
        self.assertEqual(res.status_code, status.HTTP_204_NO_CONTENT)
        ingredients = Ingredient.objects.filter(user=self.user)
        self.assertEqual(ingredients.count(), 0)
        self.assertFalse(ingredients.exists())
