from django.db import models
from django.db.models import Q
from rest_framework import serializers

from institutions.models.organization import Organization


class LibraryBook(models.Model):
    type = models.CharField(max_length=50, null=True, blank=True)
    isbn = models.CharField(max_length=100, null=False, blank=False)
    title = models.CharField(max_length=255, null=False, blank=False)
    subtitle = models.CharField(max_length=255, null=True, blank=True)
    author = models.TextField(max_length=1000, null=False, blank=False)
    publisher = models.CharField(max_length=255, null=True, blank=True)
    subject = models.TextField(max_length=1000, null=True, blank=True)
    date_published = models.DateField(null=True, blank=True)
    length_pages = models.PositiveIntegerField(null=True, blank=True)
    edition = models.CharField(max_length=255, null=True, blank=True)
    organization = models.ForeignKey(Organization, on_delete=models.CASCADE)
    cover_image = models.TextField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LibraryBookWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBook
        fields = '__all__'


class LibraryBookReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBook
        fields = '__all__'


def search_books_by_title(title) -> Q:
    if title:
        return Q(title__icontains=title)
    return Q()


def search_book_by_isbn(isbn) -> Q:
    if isbn:
        return Q(isbn__icontains=isbn)
    return Q()


def search_books_by_author(author) -> Q:
    if author:
        return Q(author__icontains=author)
    return Q()
