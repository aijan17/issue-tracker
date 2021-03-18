# Generated by Django 3.1.6 on 2021-03-14 06:51

from django.db import migrations


def transfer_tags(apps, schema_editor):
    Task = apps.get_model('webapp.Task')

    for task in Task.objects.all():
        task.types.set(task.types_old.all())


def rollback_transfer(apps, schema_editor):
    Task = apps.get_model('webapp.Task')

    for task in Task.objects.all():
        task.types_old.set(task.types.all())


class Migration(migrations.Migration):
    dependencies = [

        # Оставьте здесь свой номер миграции

        ('webapp', '0005_auto_20210314_0651'),

    ]

    operations = [

        migrations.RunPython(transfer_tags, rollback_transfer)

    ]