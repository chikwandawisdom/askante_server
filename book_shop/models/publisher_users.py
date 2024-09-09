from django.db import models
from rest_framework import serializers

from book_shop.models.publishers import PublisherReadSerializer, Publisher


class PublisherUser(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    email = models.EmailField(max_length=100)
    invitation_code = models.CharField(max_length=100, null=True, blank=True)
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    # user = models.ForeignKey('User', on_delete=models.CASCADE, null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)


class PublisherUserWriteSerializer(serializers.ModelSerializer):
    class Meta:
        model = PublisherUser
        fields = '__all__'


class PublisherUserReadSerializer(serializers.ModelSerializer):
    publisher = PublisherReadSerializer(read_only=True, many=False)

    class Meta:
        model = PublisherUser
        fields = '__all__'
