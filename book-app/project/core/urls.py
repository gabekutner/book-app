from django.urls import path
from .views import booklist, BookDetail, BookEdit

urlpatterns = [
    path('', booklist, name='books'),
    path('book/<int:pk>/', BookDetail.as_view(), name='book-detail'),
    path('book-edit/<int:pk>/', BookEdit.as_view(), name='book-edit'),
]