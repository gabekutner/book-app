from django.shortcuts import render, redirect
from django.views import generic
from django.urls import reverse_lazy
from django.db import IntegrityError

from datetime import datetime

from .models import Book, BookContributor, Contributor, Review

# Create your views here.
def booklist(request):

    # if request.GET == 'add-to-book-list' --> update(book_started=True, date_started=datetime.now())
    if request.GET.get('add-to-book-list') == 'Add':
        # test
        print(request.method)
        query = request.GET.get('hidden-book')
        book = Book.objects.filter(pk=query).update(book_started=True, date_started=datetime.now())
        # clear url
        return redirect('books')

    # if request.GET == 'back' --> update(book_started=False, date_started=None)
    if request.GET.get('back') == 'back':
        # test
        print(request.method)
        query = request.GET.get('hidden-book-back')
        book = Book.objects.filter(pk=query).update(book_started=False, date_started=None)
        # clear url
        return redirect('books')

    # if request.POST (AddBook form) --> create new book w title, am_link attrs
    if request.POST.get('AddBook') == 'AddBook':
        # test
        print(request.method)
        query1 = request.POST.get('utitle')
        # get this auto
        query2 = request.POST.get('ulink')
        query3 = request.POST.get('uauthor-f')
        query4 = request.POST.get('uauthor-l')

        # make book
        book = Book.objects.create(title=query1, am_link=query2)

        # make contributor
        try:
            Contributor.objects.create(first_names=query3, last_names=query4)
        except IntegrityError: 
            contributor = Contributor.objects.get(first_names=query3, last_names=query4)
        
        # make relationship between book and contributor
        BookContributor.objects.create(book=book, contributor=contributor, role='AUTHOR')


    ''' How to order list of models by two attributes? 
        -date_started works, but book_finished?'''
    sorted_books = Book.objects.order_by('-date_started')

    context = {'books': sorted_books}
    return render(request, 'core/book-list.html', context)

class BookDetail(generic.DetailView):
    model = Book
    context_object_name = 'book'
    template_name = 'core/book-detail.html'

class BookEdit(generic.UpdateView):
    model = Book
    fields = ['title', 'am_link', 'isbn', 'contributors', ]
    template_name = 'core/book-edit.html'
    success_url = reverse_lazy('books')