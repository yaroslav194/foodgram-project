from django.contrib import admin

from .models import Ingredient, Recipe, RecipeIngredient


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "pub_date", "author")
    search_fields = ("title",)
    list_filter = ("pub_date",)


admin.site.register(Recipe)
admin.site.register(RecipeIngredient)
admin.site.register(Ingredient)
