from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('book/<int:book_id>/', views.book_detail, name='book_detail'),
    path('borrow/', views.borrow_book, name='borrow_book'),
    path('member/<int:member_id>/select-books/', views.select_books_to_borrow, name='select_books_to_borrow'),
    path('return/<int:borrow_id>/', views.return_book, name='return_book'),
    path('borrowings/', views.borrowing_list, name='borrowing_list'),
    path('member/<int:member_id>/', views.member_detail, name='member_detail'),
    path('authors/', views.authors_list, name='authors_list'),
    path('author/<int:author_id>/', views.author_detail, name='author_detail'),
    path('members/', views.members_list, name='members_list'),
    path('chatbot/', views.chatbot_page, name='chatbot'),
    path('api/chatbot/', views.chatbot_api, name='chatbot_api'),
]
