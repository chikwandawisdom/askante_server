from rest_framework.urls import path

from .views import LibraryBookList, LibraryBookDetail, LibraryBookCopyList, LibraryBookCopyDetail, \
    get_student_lending_books, get_librarian_reports, get_daily_reports

urlpatterns = [
    path('library/books', LibraryBookList.as_view(), name='library_book_list'),
    path('library/books/<int:pk>', LibraryBookDetail.as_view(), name='library_book_detail'),

    path('library/copies', LibraryBookCopyList.as_view(), name='library_book_copy_list'),
    path('library/copies/<int:pk>', LibraryBookCopyDetail.as_view(), name='library_book_copy_detail'),

    path('library/student/lending', get_student_lending_books, name='get_student_lending_books'),

    path('librarian/reports', get_librarian_reports, name='get_total_checked_out_books'),
    path('librarian/daily-reports', get_daily_reports, name='get_daily_reports'),
]
