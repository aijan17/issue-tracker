# Generated by Django 3.1.6 on 2021-03-14 06:48

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0003_auto_20210313_1529'),
    ]

    operations = [
        migrations.RenameField(
            model_name='task',
            old_name='types',
            new_name='types_old',
        ),
    ]
