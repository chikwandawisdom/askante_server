from rest_framework.urls import path

from .views import PublishersList, PublisherDetail, PublisherUsersList, BookList, BookDetail, filter_books, \
    purchase_book, get_students_purchased_books, get_purchased_books,get_books_stat_for_publisher

urlpatterns = [
    path('publishers', PublishersList.as_view(), name='publishers_list'),
    path('publishers/<int:pk>', PublisherDetail.as_view(), name='publisher_detail'),

    path('publishers/users', PublisherUsersList.as_view(), name='publisher_users_list'),
    path('books', BookList.as_view(), name='book_list'),
    path('books/<int:pk>', BookDetail.as_view(), name='book_detail'),

    path('books/filter', filter_books, name='filter_books'),
    path('books/purchase', purchase_book, name='purchase_book'),
    path('books/purchased', get_students_purchased_books, name='get_students_purchased_books'),
    path('books/admin/purchased', get_purchased_books, name='get_purchased_books'),

    path('books/publisher/stats',get_books_stat_for_publisher, name='get_books_stat_for_publisher')
]
