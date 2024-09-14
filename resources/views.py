from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated

from .models import ResourceReadSerializer, ResourceWriteSerializer, Resource
from fundamentals.custom_responses import success_w_data, success_w_msg





class ResourceList(APIView):
    """
        Create or get Resources
    """
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = ResourceWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return success_w_data(serializer.errors)

    @staticmethod
    def get(request):
        Resources = Resource.objects.objects.all().order_by('-id')
        serializer = ResourceReadSerializer(Resources, many=True)
        return success_w_data(serializer.data)


class ResourceDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        Resource = Resource.objects.get(pk=pk)
        serializer = ResourceReadSerializer(Resource)
        return success_w_data(serializer.data)

    @staticmethod
    def put(request, pk):
        Resource = Resource.objects.get(pk=pk)
        data = request.data.copy()

        serializer = ResourceWriteSerializer(Resource, data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return success_w_data(serializer.errors)

    @staticmethod
    def delete(request, pk):
        Resource = Resource.objects.get(pk=pk)
        Resource.delete()
        return success_w_data('Resource deleted successfully.')
