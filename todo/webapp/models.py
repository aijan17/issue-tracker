from django.db import models
from django.urls import reverse

from .Validator import TaskCreateForm, MinLengthValidator

b = ['@', "$", '!', '#', '%', '^', '*', '~']


class Project(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, verbose_name='Заголовок')
    desc = models.TextField(max_length=200, verbose_name='Описание')
    begin_date = models.DateField('date')
    expiration_date = models.DateField(blank=False)
    project_task = models.ManyToManyField('Task', verbose_name='Задачи', related_name='projects')

    def __str__(self):
        return '{}: {}'.format(self.pk, self.title, self.desc)


class Projects_tasks(models.Model):
    id = models.AutoField(primary_key=True)
    tasks_of_project = models.ManyToManyField('Project', blank=True)
    title = models.CharField(max_length=200, null=False, blank=False)
    value = models.CharField(max_length=200, null=False, blank=False)

    def __str__(self):
        return '{}: {}'.format(self.id, self.title, self.value, self.tasks_of_project)

    class Meta:
        verbose_name = 'Задача проекта'
        verbose_name_plural = 'Задачи проекта'


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    summary = models.CharField(max_length=100, validators=(MinLengthValidator(5),))
    status = models.ForeignKey('Status', on_delete=models.PROTECT, verbose_name='Статус', null=True, )
    types = models.ManyToManyField('Type', blank=True, related_name='types')
    description = models.CharField(max_length=200, validators=(TaskCreateForm(b),))
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.pk, self.summary, self.description)

    def get_absolute_url(self):
        return reverse('task', kwargs={'pk': self.pk})

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    value = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return '{}: {}'.format(self.pk, self.title, self.value)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(models.Model):
    id = models.AutoField(primary_key=True)
    tasks = models.ManyToManyField('Task', blank=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    value = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return '{}: {}'.format(self.id, self.title, self.value, self.tasks)

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
