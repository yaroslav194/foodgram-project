from django import forms

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'cooking_time', 'image',
                  'description', 'tags']
        help_texts = {
            'text': 'напиши что-то важное',
        }
