from django.urls import path
from . import views

urlpatterns = [
    path('books/<str:title>', views.book_list),
    path('books/<int:pk>/', views.book_detail),
    path('borrow/', views.borrow_book),
    path('return/', views.return_book),
]