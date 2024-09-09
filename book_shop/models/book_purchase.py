from django.db import models

from rest_framework import serializers

from book_shop.models.books import Book
from students.models.students import Student


class BookPurchase(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, null=True, blank=True)
    student = models.ForeignKey(Student, on_delete=models.CASCADE)
    total_price = models.PositiveIntegerField()
    purchase_date = models.DateTimeField(auto_now_add=True)
    book_url = models.TextField(max_length=1000)
    payment_gateway_token = models.CharField(max_length=255, null=True, blank=True)


class BookPurchaseReadSerializer(serializers.ModelSerializer):
    class Meta:
        model = BookPurchase
        fields = '__all__'
        depth = 1
