# Generated by Django 3.2 on 2021-04-19 10:29

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('accounts', '0004_auto_20210418_1755'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='profile',
            options={'permissions': [('manage_lead', 'Просмотр профилей')], 'verbose_name': 'Профиль', 'verbose_name_plural': 'Профили'},
        ),
    ]