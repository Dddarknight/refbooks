from django.db import models
from django.utils import timezone


class RefBook(models.Model):
    class Meta:
        verbose_name = 'refbook'
        verbose_name_plural = 'refbooks'

        ordering = ['code']

    code = models.CharField(max_length=100, blank=False, unique=True)
    name = models.CharField(max_length=300, blank=False)
    description = models.TextField()

    def __str__(self):
        return f'refbook {self.name} (code {self.code})'


class Version(models.Model):

    refbook = models.ForeignKey(RefBook, on_delete=models.CASCADE)
    version = models.CharField(max_length=50, blank=False)
    start_date = models.DateField(default=timezone.now)

    class Meta:
        verbose_name = 'version'
        verbose_name_plural = 'versions'

        unique_together = [
            ['refbook', 'version'],
            ['refbook', 'start_date'],
        ]
        ordering = ['version']

    def __str__(self):
        return f'{self.refbook}, version {self.version}'


class Element(models.Model):

    version = models.ForeignKey(Version, on_delete=models.CASCADE)
    code = models.CharField(max_length=100, blank=False)
    value = models.CharField(max_length=300, blank=False)

    class Meta:
        verbose_name = 'element'
        verbose_name_plural = 'elements'

        unique_together = ['version', 'code']
        ordering = ['code']

    def __str__(self):
        return self.value
