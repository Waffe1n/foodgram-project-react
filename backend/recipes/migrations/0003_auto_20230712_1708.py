# Generated by Django 3.2.16 on 2023-07-12 12:08

import django.core.validators
from django.db import migrations, models

import recipes.validators


class Migration(migrations.Migration):

    dependencies = [
        ('recipes', '0002_initial'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='cart',
            options={'ordering': ['user'], 'verbose_name': 'Список покупок', 'verbose_name_plural': 'Списки покупок'},
        ),
        migrations.AlterModelOptions(
            name='favoriterecipe',
            options={'verbose_name': 'Избранный рецепт', 'verbose_name_plural': 'Избранные рецепты'},
        ),
        migrations.AlterModelOptions(
            name='follow',
            options={'ordering': ['user'], 'verbose_name': 'Подписка', 'verbose_name_plural': 'Подписки'},
        ),
        migrations.AlterModelOptions(
            name='ingredient',
            options={'ordering': ['name'], 'verbose_name': 'Ингредиент', 'verbose_name_plural': 'Ингредиенты'},
        ),
        migrations.AlterModelOptions(
            name='recipe',
            options={'ordering': ['-pub_date'], 'verbose_name': 'Рецепт', 'verbose_name_plural': 'Рецепты'},
        ),
        migrations.AlterModelOptions(
            name='recipeingredient',
            options={'ordering': ['recipe'], 'verbose_name': 'Ингредиенты в рецепте', 'verbose_name_plural': 'Ингредиенты в рецептах'},
        ),
        migrations.AlterModelOptions(
            name='tag',
            options={'ordering': ['name'], 'verbose_name': 'Тег', 'verbose_name_plural': 'Теги'},
        ),
        migrations.AlterField(
            model_name='recipeingredient',
            name='amount',
            field=models.PositiveSmallIntegerField(validators=[django.core.validators.MinValueValidator], verbose_name='количество'),
        ),
        migrations.AlterField(
            model_name='tag',
            name='color',
            field=models.CharField(max_length=7, unique=True, validators=[recipes.validators.color_validation], verbose_name='Цвет'),
        ),
    ]
