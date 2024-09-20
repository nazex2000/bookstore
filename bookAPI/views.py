from django.shortcuts import render
from rest_framework import viewsets
from .models import Book, BookCategory
from .serializers import BookSerializer, BookCategorySerializer

# Create your views here.

class BookCategoryViewSet(viewsets.ModelViewSet):
    queryset = BookCategory.objects.all()
    serializer_class = BookCategorySerializer
