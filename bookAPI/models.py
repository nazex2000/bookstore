from django.db import models

# Create your models here.
class BookCategory(models.Model):
    category = models.CharField(max_length=100, unique=True)

    def __str__(self):
        return self.category

class Book(models.Model):
    title = models.CharField(max_length=100, unique=True)
    author = models.CharField(max_length=100, null=False)
    category = models.ForeignKey(BookCategory, on_delete=models.PROTECT, default=1)
    publication_date = models.DateField(null=False)
    isbn = models.CharField(max_length=13, unique=True)
    price = models.DecimalField(max_digits=5, decimal_places=2, null=False)

    def __str__(self):
        return self.title + ' by ' + self.author