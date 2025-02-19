from django.shortcuts import render

# Create your views here.
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .models import Book, BorrowRecord
from .serializers import BookSerializer, BorrowRecordSerializer
from django.utils import timezone
from datetime import timedelta

@api_view(['GET', 'POST'])
def book_list(request):
    if request.method == 'GET':
        title = request.query_params.get('title', None)
        if title is None:
            books = Book.objects.all()
        if title is not None:
            books = Book.objects.fitler(title=title)
            if books.count() <= 0:
                return Response({"error": "no book find"}, status=status.HTTP_400_BAD_REQUEST)
            if books.count() > 0:
                serializer = BookSerializer(books, many=True)
                return Response(serializer.data)
    elif request.method == 'POST':
        serializer = BookSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

@api_view(['GET', 'PUT', 'DELETE'])
def book_detail(request, pk):
    try:
        book = Book.objects.get(pk=pk)
    except Book.DoesNotExist:
        return Response(status=status.HTTP_404_NOT_FOUND)

    if request.method == 'GET':
        serializer = BookSerializer(book)
        return Response(serializer.data)
    elif request.method == 'PUT':
        serializer = BookSerializer(book, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'DELETE':
        book.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)

@api_view(['POST'])
def borrow_book(request):
    user = request.user
    book_id = request.data.get('book_id')
    try:
        book = Book.objects.get(pk=book_id)
    except Book.DoesNotExist:
        return Response({"error": "Book not found"}, status=status.HTTP_404_NOT_FOUND)

    if book.quantity <= 0:
        return Response({"error": "No copies available"}, status=status.HTTP_400_BAD_REQUEST)

    due_date = timezone.now().date() + timedelta(days=30)
    borrow_record = BorrowRecord.objects.create(user=user, book=book, due_date=due_date)
    book.quantity -= 1
    book.save()

    serializer = BorrowRecordSerializer(borrow_record)
    return Response(serializer.data, status=status.HTTP_201_CREATED)

@api_view(['POST'])
def return_book(request):
    user = request.user
    book_id = request.data.get('book_id')
    try:
        borrow_record = BorrowRecord.objects.get(user=user, book_id=book_id, returned=False)
    except BorrowRecord.DoesNotExist:
        return Response({"error": "Borrow record not found"}, status=status.HTTP_404_NOT_FOUND)

    borrow_record.returned = True
    borrow_record.save()
    book = borrow_record.book
    book.quantity += 1
    book.save()

    return Response({"message": "Book returned successfully"}, status=status.HTTP_200_OK)