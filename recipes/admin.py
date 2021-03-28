from django.contrib import admin

from .models import Recipe, RecipeIngredients, Ingredient


class PostAdmin(admin.ModelAdmin):
    list_display = ("pk", "title", "pub_date", "author")
    search_fields = ("title",)
    list_filter = ("pub_date",)


admin.site.register(Recipe)
admin.site.register(RecipeIngredients)
admin.site.register(Ingredient)
