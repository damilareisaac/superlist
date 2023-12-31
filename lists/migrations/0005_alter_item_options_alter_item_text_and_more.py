# Generated by Django 4.2 on 2023-07-14 22:06

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("lists", "0004_item_list"),
    ]

    operations = [
        migrations.AlterModelOptions(
            name="item",
            options={"ordering": ("id",)},
        ),
        migrations.AlterField(
            model_name="item",
            name="text",
            field=models.TextField(default="", unique=True),
        ),
        migrations.AlterUniqueTogether(
            name="item",
            unique_together={("list", "text")},
        ),
    ]
