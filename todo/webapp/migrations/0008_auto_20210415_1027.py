# Generated by Django 3.1.6 on 2021-04-15 10:27

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20210415_0952'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='project',
            options={'permissions': [('add_delete_user', 'Добавление и удаление пользователя')], 'verbose_name': 'Проект', 'verbose_name_plural': 'Проекты'},
        ),
    ]
