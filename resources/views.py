from django.shortcuts import render
from django.db.models import Q
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated
from django.contrib.postgres.search import SearchQuery, SearchVector, SearchRank

from fundamentals.custom_responses import success_w_msg, success_w_data, err_w_serializer, err_w_msg, \
    get_paginated_response
from .models import ResourceReadSerializer, ResourceWriteSerializer, Resource
from fundamentals.custom_responses import success_w_data, success_w_msg
from .queries import ( filter_by_grade, filter_by_level, 
                      filter_by_subject, filter_by_syllabus, filter_by_type, search_by_name )


class ResourceList(APIView):
    """
        Create or get Resources
    """
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):

        data = request.data.copy()
        data['posted_by'] = request.user.id

        serializer = ResourceWriteSerializer(data=data)
        print(data)
        if serializer.is_valid():
            print('valid post!!!')
            serializer.save()
            return success_w_data(serializer.data)
        return success_w_data(serializer.errors)

    @staticmethod
    def get(request):

        params = request.query_params
        # queryset = Resource.objects.filter(
        #     Q(search_by_name(params.get('search'),))
        #     & filter_by_level(params.get('level'))
        #     & filter_by_type(params.get('type'))
        #     & filter_by_subject(params.get('subject'))
        #     & filter_by_syllabus(params.get('syllabus'))
        #     & filter_by_grade(params.get('grade'))
        # ).order_by('-created_at')
        # return get_paginated_response(request, queryset, ResourceReadSerializer)

        posts = Resource.objects.all()
        search_vector = SearchVector("name", weight="A") + SearchVector(
            "description", weight="C"
        )
        search_query = SearchQuery(params.get('search'))
        queryset = posts.annotate(
            search=search_vector, rank=SearchRank(search_vector, search_query)
        ).filter(
            Q(search=search_query)
            & filter_by_level(params.get('level'))
            & filter_by_type(params.get('type'))
            & filter_by_subject(params.get('subject'))
            & filter_by_syllabus(params.get('syllabus'))
            & filter_by_grade(params.get('grade'))
        ).order_by("-rank")

        return get_paginated_response(request, queryset, ResourceReadSerializer)
        
        



class ResourceDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        resource = Resource.objects.filter(id=pk).first()
        if not resource:
            return err_w_msg('Resource not found.')
        serializer = ResourceReadSerializer(resource)
        return success_w_data(serializer.data)

    @staticmethod
    def patch(request, pk):

        resource = Resource.objects.filter(id=pk).first()
        if not resource:
            return err_w_msg('Resource not found.')

        serializer = ResourceWriteSerializer(resource, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_msg('Resource updated successfully.')
        return err_w_serializer(serializer)

    @staticmethod
    def delete(request, pk):
        resource = Resource.objects.filter(id=pk).first()
        if not resource:
            return err_w_msg('Resource not found.')
        resource.delete()
        return success_w_msg('Resource deleted successfully.')
