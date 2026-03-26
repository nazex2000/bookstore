from rest_framework import generics
from rest_framework.response import Response
from .models import Book, BookCategory
from .serializers import BookSerializer, BookCategorySerializer
from rest_framework.filters import SearchFilter
from django.core.paginator import Paginator, EmptyPage
from django.core.cache import cache
from .cache_utils import (
    BOOK_LIST_CACHE_TTL_SECONDS,
    build_book_list_cache_key,
    normalize_list_params,
)

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
        category = self.request.query_params.get('category')
        price_from = self.request.query_params.get('price_from')
        price_to = self.request.query_params.get('price_to')
        ordering = self.request.query_params.get('ordering')
        queryset = Book.objects.all()
        if category:
            queryset = queryset.filter(category__id=category)
        if price_from:
            queryset = queryset.filter(price__gte=price_from)
        if price_to:
            queryset = queryset.filter(price__lte=price_to)
        if ordering:
            ordering_fieds = [field.strip() for field in ordering.split(',') if field.strip()]
            queryset = queryset.order_by(*ordering_fieds)
        return queryset

    def list(self, request, *args, **kwargs):
        normalized_params = normalize_list_params(request.query_params)
        queryset = self.get_queryset()

        paginator = Paginator(queryset, normalized_params["perpage"])
        try:
            page_obj = paginator.page(number=normalized_params["page"])
        except EmptyPage:
            page_obj = paginator.page(number=paginator.num_pages)

        cache_key = build_book_list_cache_key(normalized_params)
        cached_payload = cache.get(cache_key)
        if cached_payload is not None:
            return Response(cached_payload)

        serializer = self.get_serializer(page_obj.object_list, many=True)
        payload = {
            "count": paginator.count,
            "num_pages": paginator.num_pages,
            "current_page": page_obj.number,
            "results": serializer.data,
        }
        cache.set(cache_key, payload, BOOK_LIST_CACHE_TTL_SECONDS)
        return Response(payload)

class BookDetailViewSet(generics.RetrieveUpdateDestroyAPIView):
    queryset = Book.objects.all()
    serializer_class = BookSerializer