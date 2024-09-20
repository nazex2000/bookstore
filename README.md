Project Overview: Bookstore API
Model Design:

Create a Book model with fields like title, author, publication date, ISBN, and price. This model will represent the books in your bookstore.
Validation and Sanitization:

Use DRF serializers to handle input data. Implement validations to ensure:
Required fields are present.
ISBN format is correct and unique.
Price is a positive value.
Custom validation methods in the serializer will help sanitize input data.
Search, Ordering, Filtering, and Pagination:

Implement a viewset for the Book model that allows CRUD operations.
Use Django Filter to enable filtering by author and other fields.
Incorporate DRF’s search and ordering functionalities to allow clients to search for books by title and author and order results based on publication date or price.
Implement pagination to manage large datasets, providing a more user-friendly API experience.
Caching Strategies:

Utilize Django's caching framework to optimize performance:
In-Memory Caching: Cache the list of books to reduce database queries for frequently accessed data.
View Caching: Use decorators like @cache_page for views that return static data.
Per-Object Caching: Cache individual book instances when retrieved to speed up subsequent requests for the same book.
