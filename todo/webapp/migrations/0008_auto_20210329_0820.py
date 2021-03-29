# Generated by Django 3.1.6 on 2021-03-29 08:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0007_auto_20210329_0748'),
    ]

    operations = [
        migrations.AlterModelOptions(
            name='projects_tasks',
            options={'verbose_name': 'Задача проекта', 'verbose_name_plural': 'Задачи проекта'},
        ),
        migrations.AlterField(
            model_name='projects_tasks',
            name='tasks_of_project',
            field=models.ManyToManyField(blank=True, to='webapp.Project', verbose_name='Проекты'),
        ),
    ]