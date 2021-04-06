from taggit.models import Tag

from recipes.models import RecipeIngredient, Ingredient


def get_tags(request):
    tags_from_get = []
    if 'tags' in request.GET:
        tags_from_get = request.GET.get('tags')
        _ = tags_from_get.split(',')
        tags_qs = Tag.objects.filter(slug__in=_).values('slug')
    else:
        tags_qs = False
    return [tags_qs, tags_from_get]


def get_ingredients(data):
    ingredient_numbers = set()
    ingredients = []
    for key in data:
        if key.startswith('nameIngredient_'):
            _, number = key.split('_')
            ingredient_numbers.add(number)
    for number in ingredient_numbers:
        ingredients.append(
            {
                'name': data[f'nameIngredient_{number}'],
                'unit': data[f'unitsIngredient_{number}'],
                'quantity': float(data[f'valueIngredient_{number}']),
            }
        )
    return ingredients


def save_recipe(recipe, ingredients, request):
    recipe.author = request.user
    recipe.save()
    for item in ingredients:
        receipting = RecipeIngredient(
            quantity=item.get('quantity'),
            ingredient=
            Ingredient.objects.get_object_or_404(name=item.get('name')),
            recipe=recipe)
        receipting.save()
