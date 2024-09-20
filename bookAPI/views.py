from django.shortcuts import render
from rest_framework import generics
from .models import Book, BookCategory
from .serializers import BookSerializer, BookCategorySerializer
from rest_framework.filters import SearchFilter

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
    filter_backends = [SearchFilter]
    search_fields = ['title', 'author']

    def get_queryset(self):
        category = self.request.query_params.get('category', None)
        price_from = self.request.query_params.get('price_from', None)
        price_to = self.request.query_params.get('price_to', None)
        queryset = Book.objects.all()
        if category:
            queryset = queryset.filter(category__id=category)
        if price_from:
            queryset = queryset.filter(price__gte=price_from)
        if price_to:
            queryset = queryset.filter(price__lte=price_to)
        return queryset

class BookDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer