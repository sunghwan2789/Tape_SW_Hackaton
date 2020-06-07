# Generated by Django 2.2.11 on 2020-06-07 19:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('api', '0006_filtersection'),
    ]

    operations = [
        migrations.AlterField(
            model_name='filtersection',
            name='video',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='filters', to=settings.AUTH_USER_MODEL),
        ),
    ]
