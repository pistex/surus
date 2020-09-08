# Generated by Django 3.1.1 on 2020-09-08 05:40

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('blog', '0005_auto_20200907_1216'),
    ]

    operations = [
        migrations.AddField(
            model_name='issue',
            name='category',
            field=models.CharField(choices=[('CODE', 'Code'), ('TYPO', 'Typo'), ('ETC', 'Etc')], default='Etc', max_length=10),
        ),
        migrations.AddField(
            model_name='issue',
            name='is_public',
            field=models.BooleanField(default=False),
        ),
        migrations.AddField(
            model_name='issue',
            name='is_solved',
            field=models.BooleanField(default=False),
        ),
        migrations.DeleteModel(
            name='HistoricalIssue',
        ),
    ]
