from django import forms
from django.core.exceptions import ValidationError

from .models import Recipe


class RecipeForm(forms.ModelForm):
    class Meta:
        model = Recipe
        fields = ['title', 'cooking_time', 'image',
                  'descriptions', 'tags']
        help_texts = {
            'text': 'напиши что-то важное',
        }
