from django.urls import path
from .views import BookCategoryViewSet, BookCategoryDetailViewSet, BookViewSet, BookDetailViewSet

urlpatterns = [
    path('bookcategory/', BookCategoryViewSet.as_view()),
    path('bookcategory/<int:pk>/', BookCategoryDetailViewSet.as_view()),
    path('book/', BookViewSet.as_view()),
    path('book/<int:pk>/', BookDetailViewSet.as_view())
]