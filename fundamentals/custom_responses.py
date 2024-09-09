import json

from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.status import HTTP_400_BAD_REQUEST, HTTP_401_UNAUTHORIZED, HTTP_200_OK, HTTP_403_FORBIDDEN


def err_w_msg(msg: object, status: object = HTTP_400_BAD_REQUEST) -> object:
    """
    returns an error api response with given message and status code
    :param msg: String
    :param status: Int
    :return: Response
    """
    return Response({'err': True, 'msg': msg}, status=status if status is not None else HTTP_400_BAD_REQUEST)


def err_no_auth():
    """
    return an unauthorized api response with 401 status code
    :return: Response
    """
    return Response({'err': True, 'msg': 'You are not authorized to perform this action'}, status=HTTP_401_UNAUTHORIZED)


def err_forbidden():
    """
    return an forbidden api response with 403 status code
    :return: Response
    """
    return Response({'err': True, 'msg': 'You are forbidden from performing this action'}, status=HTTP_403_FORBIDDEN)


def err_w_serializer(errors):
    """
    returns an error api response with processed error message from the serializer errors with 400 status code
    :param errors:
    :return:
    """

    err_msg = ''

    try:
        for index, err in enumerate(errors):

            end_char = '' if index == (len(errors) - 1) else '\n'
            if type(errors[err]) is list:
                err_msg = err_msg + err + " - " + errors[err][0] + end_char
            elif type(errors[err]) is dict:
                err_msg = err_msg + err + " - " + json.dumps(errors[err], indent=0, sort_keys=True,
                                                             default=str) + end_char
    except Exception as e:
        # convert errors to string
        err_msg = str(errors)

    return Response({'err': True, 'msg': err_msg}, status=HTTP_400_BAD_REQUEST)


def success_w_msg(msg, status=HTTP_200_OK):
    """
        returns a success api response with given message and status code
        :param msg: String
        :param status: Int
        :return: Response
        """
    return Response({'err': False, 'msg': msg}, status=status if status is not None else HTTP_200_OK)


def success_w_data(data, msg='Success', status=HTTP_200_OK):
    """
        returns a success api response with given message and status code
        :param data:
        :param msg: String
        :param status: Int
        :return: Response
        """

    return Response({'msg': msg, 'err': False, 'results': data}, status=status)


def get_paginated_response(request, queryset, serializer):
    """
    returns a paginated response
    :param request: request.query_params
    :param queryset: Queryset
    :param serializer: Serializer
    :return: Response
    """
    params = request.query_params

    # paginator settings
    paginator = PageNumberPagination()
    paginator.page_size = params.get('limit') if params.get('limit') else 10

    raw_data = paginator.paginate_queryset(queryset, request)
    data = serializer(raw_data, many=True, context={'request': request}).data

    return paginator.get_paginated_response(data)
