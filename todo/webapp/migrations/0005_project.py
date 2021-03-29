# Generated by Django 3.1.6 on 2021-03-25 15:40

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('webapp', '0004_auto_20210325_1104'),
    ]

    operations = [
        migrations.CreateModel(
            name='Project',
            fields=[
                ('id', models.AutoField(primary_key=True, serialize=False)),
                ('title', models.CharField(max_length=100, verbose_name='Заголовок')),
                ('desc', models.TextField(max_length=200, verbose_name='Описание')),
                ('begin_date', models.DateField(verbose_name='date')),
                ('expiration_date', models.DateField()),
                ('project_task', models.ForeignKey(null=True, on_delete=django.db.models.deletion.PROTECT, to='webapp.task', verbose_name='Проект')),
            ],
        ),
    ]