import os
import requests

from django.db.models import Q
from rest_framework import status
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from nanoid import generate

from fundamentals.custom_responses import success_w_data, success_w_msg, get_paginated_response
from fundamentals.email import send_email
from students.models.students import Student
from .models.book_purchase import BookPurchase, BookPurchaseReadSerializer
from .models.publishers import Publisher, PublisherWriteSerializer, PublisherReadSerializer
from .models.publisher_users import PublisherUser, PublisherUserWriteSerializer, PublisherUserReadSerializer
from .models.books import Book, BookWriteSerializer, BookReadPrivateSerializer, BookReadPublicSerializer

from users.permissions import IsSuperUser, IsPublisher, IsStudent


class PublishersList(APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    # override GET methods permission to IsAuthenticated only
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = PublisherWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return success_w_data(serializer.errors)

    @staticmethod
    def get(request):
        publishers = Publisher.objects.all()
        serializer = PublisherReadSerializer(publishers, many=True)
        return success_w_data(serializer.data)


class PublisherDetail(APIView):
    permission_classes = [IsAuthenticated, IsSuperUser]

    # override GET methods permission to IsAuthenticated only
    def get_permissions(self):
        if self.request.method == 'GET':
            self.permission_classes = [IsAuthenticated]
        return super().get_permissions()

    @staticmethod
    def get(request, pk):
        publisher = Publisher.objects.get(pk=pk)
        serializer = PublisherReadSerializer(publisher)
        return success_w_data(serializer.data)

    @staticmethod
    def put(request, pk):
        publisher = Publisher.objects.get(pk=pk)
        data = request.data.copy()

        serializer = PublisherWriteSerializer(publisher, data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return success_w_data(serializer.errors)

    @staticmethod
    def delete(request, pk):
        publisher = Publisher.objects.get(pk=pk)
        publisher.delete()
        return success_w_data('Publisher deleted successfully.')


class PublisherUsersList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def post(request):
        data = request.data.copy()

        data['invitation_code'] = generate()

        serializer = PublisherUserWriteSerializer(data=data)
        if serializer.is_valid():
            publisher_user = serializer.save()

            send_email(to=publisher_user.email, subject='School Management System Registration Link', body_params={
                'registration_url': f'https://askante.net/register?code={publisher_user.invitation_code}&type=publisher'
            })

            return success_w_data(serializer.data)
        return success_w_data(serializer.errors)

    @staticmethod
    def get(request):

        if request.user.is_superuser:
            publisher_users = PublisherUser.objects.all()
        else:
            publisher_users = PublisherUser.objects.filter(publisher=request.user.publisher)

        serializer = PublisherUserReadSerializer(publisher_users, many=True)
        return success_w_data(serializer.data)


class BookList(APIView):
    """
        Create or get books
    """
    permission_classes = [IsAuthenticated, IsPublisher]

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = BookWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return success_w_data(serializer.errors)

    @staticmethod
    def get(request):
        publisher = request.query_params.get('publisher')
        books = Book.objects.filter(publisher=publisher).order_by('-id')
        serializer = BookReadPrivateSerializer(books, many=True)
        return success_w_data(serializer.data)


class BookDetail(APIView):
    permission_classes = [IsAuthenticated, IsPublisher]

    @staticmethod
    def get(request, pk):
        book = Book.objects.get(pk=pk)
        serializer = BookReadPrivateSerializer(book)
        return success_w_data(serializer.data)

    @staticmethod
    def put(request, pk):
        book = Book.objects.get(pk=pk)
        data = request.data.copy()

        serializer = BookWriteSerializer(book, data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return success_w_data(serializer.errors)

    @staticmethod
    def delete(request, pk):
        book = Book.objects.get(pk=pk)
        book.delete()
        return success_w_data('Book deleted successfully.')


def search_books_by_name(search_term):
    if search_term is None:
        return Q()
    return Q(name__icontains=search_term)


def filter_books_by_grade(grade):
    if grade is None:
        return Q()
    return Q(grade=grade)


def filter_books_by_level(level):
    if level is None:
        return Q()
    return Q(level=level)


def filter_books_by_isbn(isbn):
    if isbn is None:
        return Q()
    return Q(isbn_number=isbn)


def filter_books_by_subject(subject):
    if subject is None:
        return Q()
    return Q(subject=subject)

def filter_books_by_publisher(publisher):
    if publisher is None:
        return Q()
    return Q(publisher=publisher)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def filter_books(request):
    params = request.query_params
    queryset = Book.objects.filter(
        search_books_by_name(params.get('search_term'))
        & filter_books_by_grade(params.get('grade'))
        & filter_books_by_level(params.get('level'))
        & filter_books_by_isbn(params.get('isbn'))
        & filter_books_by_subject(params.get('subject'))
         & filter_books_by_publisher(params.get('publisher'))
    ).order_by('-id'
               )
    return get_paginated_response(request=request, serializer=BookReadPublicSerializer, queryset=queryset)


@api_view(['POST'])
@permission_classes([IsAuthenticated, IsStudent])
def purchase_book(request):
    data = request.data.copy()

    book = Book.objects.get(pk=data['book'])
    if book is None:
        return success_w_data('Book not found.')

    student = Student.objects.get(user=request.user)

    try:
        yoco_api_url = 'https://online.yoco.com/v1/charges/'
        yoco_secret_key = os.getenv('YOCO_SECRET_KEY', '')

        headers = {
            'X-Auth-Secret-Key': yoco_secret_key,
        }

        response = requests.post(yoco_api_url, json=data, headers=headers)
        response_data = response.json()

        if response.status_code in [200, 201]:

            # Assuming both status codes represent successful payment
            BookPurchase.objects.create(
                book=book,
                student=student,
                total_price=book.price,
                book_url=book.book_url,
                payment_gateway_token=data.get('token')
            )

            return success_w_msg(msg='Book purchased successfully.')

        elif response.status_code == 400:
            # Add some logs when payment fails
            return Response({'status': 'not ok', 'error': response_data}, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response({'status': 'not ok', 'error': response_data}, status=response.status_code)

    except requests.RequestException as error:
        return Response({'status': 'not ok', 'error': str(error)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


def filter_book_purchase_by_book(book):
    if book is None:
        return Q()
    return Q(book=book)


def filter_book_purchase_by_publisher(publisher):
    if publisher is None:
        return Q()
    return Q(book__publisher=publisher)


def filter_book_purchase_by_level(level):
    if level is None:
        return Q()
    return Q(book__level=level)


def filter_book_purchase_by_grade(grade):
    if grade is None:
        return Q()
    return Q(book__grade=grade)


def filter_book_purchase_by_date_range(start, end):
    if start and end is not None:
        return Q(purchase_date__range=[start, end])
    return Q()


def filter_book_purchase_by_isbn(isbn):
    if isbn is None:
        return Q()
    return Q(book__isbn_number=isbn)


def filter_book_purchase_by_subject(subject):
    if subject is None:
        return Q()
    return Q(book__subject=subject)


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudent])
def get_students_purchased_books(request):
    student = Student.objects.get(user=request.user)
    purchases = BookPurchase.objects.filter(
        Q(student=student)
        & filter_book_purchase_by_isbn(request.query_params.get('isbn'))
        & filter_book_purchase_by_publisher(request.query_params.get('publisher'))
        & filter_book_purchase_by_subject(request.query_params.get('subject'))
        & filter_book_purchase_by_grade(request.query_params.get('grade'))
    )
    serializer = BookPurchaseReadSerializer(purchases, many=True)
    return success_w_data(serializer.data)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_purchased_books(request):
    purchases = BookPurchase.objects.filter(
        filter_book_purchase_by_book(request.query_params.get('book'))
        & filter_book_purchase_by_publisher(request.query_params.get('publisher'))
        & filter_book_purchase_by_level(request.query_params.get('level'))
        & filter_book_purchase_by_grade(request.query_params.get('grade'))
        & filter_book_purchase_by_date_range(request.query_params.get('start'), request.query_params.get('end'))
        & filter_book_purchase_by_subject(request.query_params.get('subject'))
    ).order_by('-id')
    serializer = BookPurchaseReadSerializer(purchases, many=True)
    return success_w_data(serializer.data)


# make a api to get total books sold, total amount $, for the selected range
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsPublisher])
def get_books_stat_for_publisher(request):
    purchases = BookPurchase.objects.filter(
        filter_book_purchase_by_date_range(request.query_params.get('start'), request.query_params.get('end'))
        & filter_book_purchase_by_publisher(request.query_params.get('publisher'))
    ).order_by('-id')
    total_books_sold = purchases.count()
    total_amount = sum([purchase.total_price for purchase in purchases])
    return success_w_data({'total_books_sold': total_books_sold, 'total_amount': total_amount})
