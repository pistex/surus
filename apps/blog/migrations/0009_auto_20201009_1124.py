# Generated by Django 3.1.2 on 2020-10-09 11:24

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0008_auto_20201009_1121'),
    ]

    operations = [
        migrations.AddField(
            model_name='image',
            name='width',
            field=models.PositiveIntegerField(default=600),
            preserve_default=False,
        ),
        migrations.AlterField(
            model_name='image',
            name='image',
            field=models.ImageField(upload_to='blog', width_field='width'),
        ),
    ]