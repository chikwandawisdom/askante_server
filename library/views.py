from django.db.models import Q
from django.utils import timezone
from rest_framework.decorators import APIView, permission_classes, api_view
from rest_framework.permissions import IsAuthenticated

from fundamentals.custom_responses import get_paginated_response, success_w_data, err_w_serializer
from students.models.students import Student
from users.permissions import IsStudent, IsLibraryManager
from .models.library_books import (LibraryBook, LibraryBookWriteSerializer, LibraryBookReadSerializer,
                                   search_book_by_isbn, search_books_by_title, search_books_by_author)
from .models.library_books_copy import (LibraryBooksCopy, LibraryBookCopyWriteSerializer,
                                        LibraryBookCopyReadSerializer, filter_by_library_book, filter_by_institution)


class LibraryBookList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        params = request.query_params
        books = LibraryBook.objects.filter(
            Q(organization=request.user.organization)
            & search_books_by_title(params.get('title'))
            & search_book_by_isbn(params.get('isbn'))
            & search_books_by_author(params.get('author'))
        ).order_by('-id')
        return get_paginated_response(request, books, LibraryBookReadSerializer)

    @staticmethod
    def post(request):
        data = request.data.copy()
        data['organization'] = request.user.organization.id

        serializer = LibraryBookWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)


class LibraryBookDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        book = LibraryBook.objects.filter(id=pk, organization=request.user.organization).first()

        if not book:
            return err_w_serializer('Book not found.')

        return success_w_data(LibraryBookReadSerializer(book, many=False).data)

    @staticmethod
    def patch(request, pk):
        book = LibraryBook.objects.filter(id=pk, organization=request.user.organization).first()

        if not book:
            return err_w_serializer('Book not found.')
        serializer = LibraryBookWriteSerializer(book, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        book = LibraryBook.objects.filter(id=pk, organization=request.user.organization).first()

        if not book:
            return err_w_serializer('Book not found.')

        book.delete()
        return success_w_data('Book deleted successfully.')


class LibraryBookCopyList(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request):
        params = request.query_params
        copies = LibraryBooksCopy.objects.filter(
            Q(library_book__organization=request.user.organization)
            & filter_by_library_book(params.get('library_book'))
            & filter_by_institution(params.get('institution'))
        ).order_by('-id')
        return get_paginated_response(request, copies, LibraryBookCopyReadSerializer)

    @staticmethod
    def post(request):
        data = request.data.copy()

        serializer = LibraryBookCopyWriteSerializer(data=data)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)


class LibraryBookCopyDetail(APIView):
    permission_classes = [IsAuthenticated]

    @staticmethod
    def get(request, pk):
        copy = LibraryBooksCopy.objects.filter(id=pk, library_book__organization=request.user.organization).first()

        if not copy:
            return err_w_serializer('Copy not found.')

        return success_w_data(LibraryBookCopyReadSerializer(copy, many=False).data)

    @staticmethod
    def patch(request, pk):
        copy = LibraryBooksCopy.objects.filter(id=pk, library_book__organization=request.user.organization).first()

        if not copy:
            return err_w_serializer('Copy not found.')
        serializer = LibraryBookCopyWriteSerializer(copy, data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return success_w_data(serializer.data)
        return err_w_serializer(serializer.errors)

    @staticmethod
    def delete(request, pk):
        copy = LibraryBooksCopy.objects.filter(id=pk, library_book__organization=request.user.organization).first()

        if not copy:
            return err_w_serializer('Copy not found.')

        copy.delete()
        return success_w_data('Copy deleted successfully.')


@api_view(['GET'])
@permission_classes([IsAuthenticated, IsStudent])
def get_student_lending_books(request):
    student = Student.objects.get(user=request.user)
    purchases = LibraryBooksCopy.objects.filter(
        Q(current_lender=student)
    ).order_by('-id')
    serializer = LibraryBookCopyReadSerializer(purchases, many=True)
    return success_w_data(serializer.data)


# get librarian reports
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsLibraryManager])
def get_librarian_reports(request):
    total_checked_out_books = LibraryBooksCopy.objects.filter(
        Q(library_book__organization=request.user.organization)
        & Q(current_lender__isnull=False)
    ).count()

    total_overdue_books = LibraryBooksCopy.objects.filter(
        Q(library_book__organization=request.user.organization)
        & Q(current_lender__isnull=False)
        & Q(due_date__lt=timezone.now())
    ).count()

    return success_w_data({
        'total_checked_out_books': total_checked_out_books,
        'total_overdue_books': total_overdue_books
    })


# last 10 days daily checkout counts for chart
@api_view(['GET'])
@permission_classes([IsAuthenticated, IsLibraryManager])
def get_daily_reports(request):
    today = timezone.now().date()
    daily_counts = []
    for i in range(10):
        date = today - timezone.timedelta(days=i)
        check_out_count = LibraryBooksCopy.objects.filter(
            Q(library_book__organization=request.user.organization)
            & Q(check_out_date__date=date)
        ).count()
        check_in_count = LibraryBooksCopy.objects.filter(
            Q(library_book__organization=request.user.organization)
            & Q(check_in_date__date=date)
        ).count()
        daily_counts.append({
            'date': date,
            'check_in_count': check_in_count,
            'check_out_count': check_out_count,
        })
    return success_w_data(daily_counts)
