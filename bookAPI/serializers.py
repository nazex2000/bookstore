from rest_framework import serializers
from .models import Book, BookCategory

class BookCategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = BookCategory
        fields = '__all__'

class BookSerializer(serializers.ModelSerializer):
    category_id = serializers.IntegerField(write_only=True)
    category = BookCategorySerializer(read_only=True)
    price_after_iva = serializers.SerializerMethodField(method_name='calculate_price_after_iva')
    class Meta:
        model = Book
        fields = ['id', 'title', 'author', 'publication_date', 'isbn', 'price', 'price_after_iva','category_id', 'category']
    def calculate_price_after_iva(self, obj: Book):
        return float(obj.price) * 1.16
    def create(self, validated_data):
        category_id = validated_data.pop('category_id')
        category = BookCategory.objects.get(pk=category_id)
        book = Book.objects.create(category=category, **validated_data)
        return book
    def update(self, instance, validated_data):
        category_id = validated_data.pop('category_id')
        category = BookCategory.objects.get(pk=category_id)
        instance.category = category
        instance.title = validated_data.get('title', instance.title)
        instance.author = validated_data.get('author', instance.author)
        instance.publication_date = validated_data.get('publication_date', instance.publication_date)
        instance.isbn = validated_data.get('isbn', instance.isbn)
        instance.price = validated_data.get('price', instance.price)
        instance.save()
        return instance