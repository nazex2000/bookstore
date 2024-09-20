from django.shortcuts import render
from rest_framework import generics
from .models import Book, BookCategory
from .serializers import BookSerializer, BookCategorySerializer

# Create your views here.

class BookCategoryViewSet(generics.ListCreateAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer

class BookCategoryDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer

class BookViewSet(generics.ListCreateAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer

class BookDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer