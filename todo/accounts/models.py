from django.contrib.auth import get_user_model
from django.db import models


class Profile(models.Model):
    user = models.OneToOneField(
        get_user_model(),
        on_delete=models.CASCADE,
        verbose_name='Профиль пользователя',
        related_name='profile',
    )
    avatar = models.ImageField(upload_to='avatars', blank=True, null=True, verbose_name='Аватар')
    about_me = models.CharField(max_length=300, blank=True, null=True)
    links = models.URLField(max_length=200,blank=True, null=True)

    def __str__(self):
        return '{}: {}'.format(self.user,self.avatar, self.about_me, self.links)

    class Meta:
        db_table = 'profiles'
        verbose_name = 'Профиль'
        verbose_name_plural = 'Профили'
        permissions = [
            ('manage_lead', 'Просмотр профилей')
        ]