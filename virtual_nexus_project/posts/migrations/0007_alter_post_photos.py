# Generated by Django 5.0.1 on 2024-02-01 18:32

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('posts', '0006_postphotos_post_photos'),
    ]

    operations = [
        migrations.AlterField(
            model_name='post',
            name='photos',
            field=models.ForeignKey(limit_choices_to={'id__lte': 3}, on_delete=django.db.models.deletion.CASCADE, related_name='photos', to='posts.postphotos'),
        ),
    ]
