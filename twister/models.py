from django.db import models
from django.contrib.auth import get_user_model

import twister


User = get_user_model()

STATUS_CHOICES = (
    ('open', 'Открытое'),
    ('closed', 'Закрытое'),
    ('draft', 'Черновик')
)


class Publication(models.Model):
    name = models.CharField('heading', max_length=255, db_index=True)
    slug = models.SlugField(max_length=200, db_index=True)
    image = models.ImageField(upload_to='', blank=True)
    text = models.TextField('description')
    status = models.CharField('status', max_length=10, choices=STATUS_CHOICES)
    user = models.ForeignKey(User,
                             on_delete=models.CASCADE,
                             related_name='prod', verbose_name='author')
    created_at = models.DateTimeField('date of creation', auto_now_add=True)
    update_at = models.DateTimeField('update date', auto_now=True)

    class Meta:
        verbose_name = 'publication'
        verbose_name_plural = 'publications'

        def __str__(self):
            return self.name


class Comment(models.Model):
    publication = models.ForeignKey(Publication,
                                    on_delete=models.CASCADE,
                                    related_name='comments', verbose_name='publication')
    user = models.ForeignKey(User, on_delete=models.CASCADE,
                             related_name='comments', verbose_name='author')
    text = models.TextField('text')
    created_at = models.DateTimeField('publication date', auto_now_add=True)

    class Meta:
        verbose_name = 'comment'
        verbose_name_plural = 'comments'

    def __str__(self):
        return f'{self.publication} --> {self.user}'


class Likes(models.Model):
    liked = models.ForeignKey(Publication, on_delete=models.CASCADE,
                              related_name='ads_likes')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='author_likes')

    class Meta:
        verbose_name = 'Like'


class RatingStar(models.Model):
    value = models.SmallIntegerField('value', default=0)

    def str(self):
        return str(self.value)

    class Meta:
        verbose_name = 'Rating Star'
        verbose_name_plural = 'Rating Stars'
        ordering = ['-value']


class Rating(models.Model):
    ads = models.ForeignKey(Publication, on_delete=models.CASCADE,
                            related_name='rating')
    author = models.ForeignKey(User, on_delete=models.CASCADE,
                               related_name='rating')
    star = models.ForeignKey(RatingStar, on_delete=models.CASCADE,
                             related_name='rating')

    def str(self):
        return f'{self.star} - {self.ads}'

    class Meta:
        verbose_name = 'Rating'
        verbose_name_plural = 'Ratings'


class Favorites(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='favorites')
    publication = models.ForeignKey(Publication, on_delete=models.CASCADE, related_name='favorites')
    name = models.CharField(max_length=50, default='favorites')

    def str(self):
        return self.publication.name

