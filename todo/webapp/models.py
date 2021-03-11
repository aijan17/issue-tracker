from django.db import models


class Task(models.Model):
    id = models.AutoField(primary_key=True)
    summary = models.CharField(max_length=100, null=False, blank=False)
    description = models.CharField(max_length=2000, null=True, blank=True)
    create_date = models.DateTimeField(auto_now_add=True)
    update_date = models.DateTimeField(auto_now=True)

    def __str__(self):
        return '{}: {}'.format(self.id, self.name, self.description)

    class Meta:
        verbose_name = 'Задача'
        verbose_name_plural = 'Задачи'


class Status(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    value = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return '{}: {}'.format(self.id, self.title, self.value)

    class Meta:
        verbose_name = 'Статус'
        verbose_name_plural = 'Статусы'


class Type(models.Model):
    id = models.AutoField(primary_key=True)
    title = models.CharField(max_length=100, null=False, blank=False)
    value = models.CharField(max_length=100, null=False, blank=False)

    def __str__(self):
        return '{}: {}'.format(self.id, self.title, self.value)

    class Meta:
        verbose_name = 'Тип'
        verbose_name_plural = 'Типы'
