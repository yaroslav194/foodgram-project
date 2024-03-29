from django.contrib.auth import get_user_model
from django.db import models
from taggit.managers import TaggableManager

User = get_user_model()


class Ingredient(models.Model):
    name = models.CharField(max_length=200,
                            verbose_name='наименование ингредиента')
    unit = models.CharField(max_length=50,
                            verbose_name='мера измерения')

    class Meta:
        verbose_name = 'Ingredient'
        verbose_name_plural = 'Ingredients'

    def __str__(self):
        return f'{self.name} ({self.unit})'


class Recipe(models.Model):
    author = models.ForeignKey(
        User, on_delete=models.CASCADE,
        related_name='recipes',
        verbose_name='автор')
    title = models.CharField(max_length=400,
                             verbose_name='заголовок',
                             blank=False)
    image = models.ImageField(upload_to='recipes/',
                              blank=False, null=True,
                              verbose_name='модель изображения')
    description = models.TextField(blank=False,
                                   verbose_name='описание')
    ingredients = models.ManyToManyField(Ingredient,
                                         verbose_name='ингредиенты')
    tags = TaggableManager()
    cooking_time = models.PositiveIntegerField(blank=False,
                                               verbose_name='время приготовления')
    slug = models.SlugField(blank=False)
    pub_date = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-pub_date']

    def __str(self):
        return self.title


class RecipeIngredient(models.Model):
    recipe = models.ForeignKey(Recipe,
                               on_delete=models.CASCADE,
                               related_name='recipe_ingredients',
                               verbose_name='рецепт')
    ingredient = models.ForeignKey(Ingredient,
                                   on_delete=models.CASCADE,
                                   related_name='recipe_ingredients',
                                   verbose_name='ингредиент')
    quantity = models.PositiveIntegerField(blank=True,
                                           verbose_name='количество')

    def __str__(self):
        return self.ingredient
