from django.contrib import admin
from .models import Book, BookContributor, Contributor, Review

# Register your models here.
admin.site.register(Book)
admin.site.register(Review)
admin.site.register(BookContributor)
admin.site.register(Contributor)