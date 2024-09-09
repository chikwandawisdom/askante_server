from django.db import models
from rest_framework import serializers

from book_shop.models.publishers import Publisher
from institutions.models.grades import Grade
from institutions.models.levels import Level
from institutions.models.subjects import Subject


class Book(models.Model):
    name = models.CharField(max_length=255)
    subject = models.ForeignKey(Subject, on_delete=models.SET_NULL, null=True, blank=True)
    isbn_number = models.CharField(max_length=255, null=True, blank=True)
    description = models.TextField(max_length=5000)
    author = models.CharField(max_length=255)
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.PositiveIntegerField()
    level = models.ForeignKey(Level, on_delete=models.SET_NULL, null=True, blank=True)
    grade = models.ForeignKey(Grade, on_delete=models.SET_NULL, null=True, blank=True)
    image = models.TextField(max_length=1000, null=True, blank=True)
    book_url = models.TextField(max_length=1000)
    unit_sold = models.PositiveIntegerField(default=0)


class BookWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'


class BookReadPrivateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        fields = '__all__'
        depth = 1


class BookReadPublicSerializer(serializers.ModelSerializer):
    class Meta:
        model = Book
        exclude = ['book_url', 'unit_sold']
        depth = 1
