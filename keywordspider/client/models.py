from django.db import models


class Content(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    datee = models.CharField(max_length=255)
    news = models.TextField()

    def __str__(self):
        return self.title


class Keyword(models.Model):
    url = models.CharField(max_length=255)
    title = models.CharField(max_length=255)
    keywords = models.TextField()

    def __str__(self):
        return self.keywords


class Frequent(models.Model):
    index = models.BigIntegerField(primary_key=True)
    support = models.FloatField()
    itemsets = models.TextField()


class Confidence(models.Model):
    index = models.BigIntegerField(primary_key=True)
    front_item = models.TextField()
    back_item = models.FloatField()
