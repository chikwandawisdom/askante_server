from django.contrib import admin

from .models.publisher_users import PublisherUser
from .models.publishers import Publisher
from .models.book_purchase import BookPurchase

admin.site.register(Publisher)
admin.site.register(PublisherUser)
admin.site.register(BookPurchase)
