from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.db.models import Sum
from django.http import HttpResponse
from django.shortcuts import get_object_or_404, redirect, render
from taggit.models import Tag

from api.models import Purchase, Subscription
from foodgram.settings import ITEMS_FOR_PAGINATOR

from .forms import RecipeForm
from .models import RecipeIngredients, Recipe, User, Ingredient


def index(request):
    recipes = Recipe.objects.all()
    tags_qs, tags_from_get = get_tags(request)

    if tags_qs:
        recipes = Recipe.objects.filter(tags__slug__in=tags_qs).distinct()

    paginator = Paginator(recipes, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'recipes/index.html',
        {'recipes': recipes, 'paginator': paginator,
         'page': page, 'tags': tags_from_get}
    )


@login_required
def new_recipe(request):
    form = RecipeForm(request.POST or None, files=request.FILES or None)
    tags = Tag.objects.all()

    if form.is_valid():
        recipe = form.save(commit=False)
        ingredients = get_ingredients(request.POST)
        save_recipe(recipe, ingredients, request)
        form.save_m2m()
        return redirect('index')
    return render(request, 'recipes/formRecipe.html', {'form': form, 'tags': tags})


@login_required
def recipe_edit(request, recipe_id, username):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    ing = RecipeIngredients.objects.filter(recipe=recipe_id)
    form = RecipeForm(request.POST or None, files=request.FILES or None,
                      instance=recipe)
    tags = Tag.objects.all()
    context = {'form': form, 'recipe': recipe,
               'ingredients': ing, 'tags': tags}

    if recipe.author == request.user:
        ingredients = get_ingredients(request.POST)

        if form.is_valid():
            ing.delete()
            recipe = form.save(commit=False)
            save_recipe(recipe, ingredients, request)
            form.save_m2m()
            print(recipe.tags.all())
            return redirect('recipe', username=request.user.username,
                            recipe_id=recipe.id)

        return render(request, 'recipes/formRecipe.html', context)
    else:
        return redirect('recipe', username=request.user.username,
                        recipe_id=recipe.id)


@login_required
def recipe_delete(request, recipe_id, username):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)

    if request.user != recipe.author:
        return redirect(
            'recipe_view',
            username=username,
            recipe_id=recipe_id
        )

    recipe.delete()
    return redirect('index')


def recipe_view(request, username, recipe_id):
    recipe = get_object_or_404(Recipe, author__username=username, id=recipe_id)
    ingredients = recipe.recipeingredient.all()
    return render(request, 'recipes/recipe_view.html', {'recipe': recipe,
                                                        'ingredients': ingredients})


def profile(request, username):
    author = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(author=author)
    tags_qs, tags_from_get = get_tags(request)

    if tags_qs:
        recipes = Recipe.objects.filter(
            author=author,
            tags__slug__in=tags_qs).distinct()

    paginator = Paginator(recipes, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/index.html',
                  {'author': author, 'page': page,
                   'paginator': paginator, 'tags': tags_from_get}
                  )


@login_required
def subscriptions(request, username):
    user = get_object_or_404(User, username=username)
    subscript = User.objects.prefetch_related('recipe').filter(
        following__user=user.id)
    paginator = Paginator(subscript, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(
        request,
        'recipes/myFollow.html',
        {'page': page, 'paginator': paginator}
    )


@login_required
def favorites(request, username):
    user = get_object_or_404(User, username=username)
    recipes = Recipe.objects.filter(favourites__user=request.user)
    tags_qs, tags_from_get = get_tags(request)

    if tags_qs:
        recipes = Recipe.objects.filter(favourites__user=request.user,
                                        tags__slug__in=tags_qs).distinct()

    paginator = Paginator(recipes, ITEMS_FOR_PAGINATOR)
    page_number = request.GET.get('page')
    page = paginator.get_page(page_number)
    return render(request, 'recipes/index.html', {
        'recipes': recipes, 'paginator': paginator, 'page': page,
        'username': user, 'tags': tags_from_get
    })


@login_required
def purchases_list(request):
    recipes_list = Purchase.purchase.get_purchases_list(request.user)
    return render(request,
                  'recipes/shopList.html',
                  {'recipes_list': recipes_list}
                  )


@login_required
def download(request):
    user = request.user
    filename = f'{user.username}_list.txt'
    recipes = Purchase.purchase.get_purchases_list(user)
    all_ingredients = []
    for recipe in recipes:
        ingredients = recipe.recipeingredient.all()
        for ingredient in ingredients:
            if (any([ingr.ingredient.name == ingredient.ingredient.name for ingr in all_ingredients])) is False:
                print(ingredient.ingredient.name)
                all_ingredients.append(ingredient)
            else:
                exist_ing = [x for x in all_ingredients if x.ingredient.name == ingredient.ingredient.name][0]
                exist_ing.quantity = exist_ing.quantity + ingredient.quantity

    products = [
         (f'{i.ingredient.name} -'
          f' {i.quantity} {i.ingredient.unit}')
         for i in all_ingredients]
    content = '\n'.join(products)
    response = HttpResponse(content, content_type='text/plain')
    response['Content-Disposition'] = f'attachment; filename={filename}'
    return response


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
    recipe_ingredients = []

    for item in ingredients:
        receipting = RecipeIngredients(
            quantity=item.get('quantity'),
            ingredient=Ingredient.objects.get(name=item.get('name')),
            recipe=recipe)
        receipting.save()
