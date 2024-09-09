from django.db import models
from rest_framework import serializers

from institutions.models.institution import Institution
from library.models.library_books import LibraryBook
from students.models.students import Student


class LibraryBooksCopy(models.Model):
    status_choices = (
        ('available', 'Available'),
        ('checked_out', 'Checked Out'),
    )

    library_book = models.ForeignKey(LibraryBook, on_delete=models.CASCADE)
    copy_number = models.CharField(null=False, blank=False, max_length=50)
    location = models.CharField(max_length=50, null=False, blank=False)
    row = models.CharField(max_length=50, null=False, blank=False)
    institution = models.ForeignKey(Institution, on_delete=models.CASCADE)

    current_lender = models.ForeignKey(Student, on_delete=models.CASCADE, null=True, blank=True)
    check_out_date = models.DateTimeField(null=True, blank=True)
    due_date = models.DateTimeField(null=True, blank=True)
    check_in_date = models.DateTimeField(null=True, blank=True)
    status = models.CharField(max_length=50, choices=status_choices, default='available')

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class LibraryBookCopyWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBooksCopy
        fields = '__all__'


class LibraryBookCopyReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = LibraryBooksCopy
        fields = '__all__'
        depth = 1


def filter_by_institution(institution) -> models.Q:
    if institution:
        return models.Q(institution=institution)
    return models.Q()


def filter_by_library_book(library_book) -> models.Q:
    if library_book:
        return models.Q(library_book=library_book)
    return models.Q()