# Generated by Django 3.1.1 on 2020-10-07 08:03

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0006_auto_20201007_0732'),
    ]

    operations = [
        migrations.AlterField(
            model_name='tag',
            name='en',
            field=models.CharField(max_length=16),
        ),
    ]
