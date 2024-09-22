from django.shortcuts import render
from rest_framework import generics
from .models import Book, BookCategory
from .serializers import BookSerializer, BookCategorySerializer
from rest_framework.filters import SearchFilter
from django.core.paginator import Paginator, EmptyPage

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
        ordering = self.request.query_params.get('ordering', None)
        perpage = self.request.query_params.get('perpage', None)
        page = self.request.query_params.get('page', None)
        queryset = Book.objects.all()
        if category:
            queryset = queryset.filter(category__id=category)
        if price_from:
            queryset = queryset.filter(price__gte=price_from)
        if price_to:
            queryset = queryset.filter(price__lte=price_to)
        if ordering:
            ordering_fieds = ordering.split(',')
            queryset = queryset.order_by(*ordering_fieds)
        paginator = Paginator(queryset, perpage)
        try:
            queryset = paginator.page(number=page)
        except EmptyPage:
            queryset = paginator.page(number=paginator.num_pages)
        return queryset

class BookDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer