# Generated by Django 3.1.5 on 2021-02-08 20:30

import django.db.models.deletion
import taggit.managers
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('taggit', '0003_taggeditem_add_unique_index'),
        ('recipes', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Recipe',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('title', models.CharField(max_length=400, verbose_name='заголовок')),
                ('image', models.ImageField(null=True, upload_to='recipes/', verbose_name='модель изображения')),
                ('description', models.TextField(verbose_name='описание')),
                ('cooking_time', models.PositiveIntegerField(verbose_name='время приготовления')),
                ('slug', models.SlugField()),
                ('pub_date', models.DateTimeField(auto_now_add=True)),
                ('author', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipe',
                                             to=settings.AUTH_USER_MODEL, verbose_name='автор')),
                ('ingredients', models.ManyToManyField(to='recipes.Ingredient', verbose_name='ингредиенты')),
                ('tags', taggit.managers.TaggableManager(help_text='A comma-separated list of tags.',
                                                         through='taggit.TaggedItem', to='taggit.Tag',
                                                         verbose_name='Tags')),
            ],
            options={
                'ordering': ['-pub_date'],
            },
        ),
        migrations.CreateModel(
            name='RecipeIngredients',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('quantity', models.PositiveIntegerField(blank=True)),
                ('ingredient', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipeingredient', to='recipes.ingredient')),
                ('recipe', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='recipeingredient', to='recipes.recipe')),
            ],
        ),
    ]
