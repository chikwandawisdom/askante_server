from django.db import models


class ZarRate(models.Model):
    date = models.DateField()
    rate = models.CharField(max_length=10)

    def __str__(self):
        return f'{self.date} - {self.rate}'
