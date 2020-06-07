# Generated by Django 2.2.11 on 2020-06-07 16:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('api', '0005_auto_20190831_0530'),
    ]

    operations = [
        migrations.CreateModel(
            name='FilterSection',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('start_time', models.FloatField()),
                ('end_time', models.FloatField()),
                ('word', models.CharField(max_length=10)),
                ('video', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
