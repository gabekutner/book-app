from django.db import models
from django.utils.translation import gettext_lazy as _
from django.core.validators import MaxValueValidator

from .utils import wb_pg_num, wb_author


# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=70, 
                            help_text="The title of the book.")
    # webscraped
    am_link = models.URLField(blank=False, 
                                verbose_name=_("Amazon Link"))
    contributors = models.ManyToManyField('Contributor', through='BookContributor')
    notes = models.TextField(null=True, blank=True, 
                            help_text="Notes for the book.")
    book_started = models.BooleanField(default=False, verbose_name=_("Book Started?"))
    book_finished = models.BooleanField(default=False,
                                verbose_name=_("Book Finished?"))
    max_pg_num = models.PositiveIntegerField(blank=True, verbose_name=_("The page length of the book."))
    isbn = models.CharField(blank=True, max_length=20, 
                            help_text="The ISBN number of the book.")
    # for ordering by
    date_started = models.DateTimeField(null=True, blank=True, verbose_name=_("Date the book was started."))

    # webscrapes max_pg_num
    def save(self, *args, **kwargs):
        if not self.id:
            self.max_pg_num = wb_pg_num(url=self.am_link)

            # ValueError / "<Book: Everyone Communicates, Few Connect 2>" needs to have a value for field "id" before this many-to-many relationship can be used.
            # 
            

            # TypeError / Direct assignment to the forward side of a many-to-many set is prohibited. Use contributors.set() instead.
            #self.contributors = wb_author(url=self.am_link)

        return super(Book, self).save(*args, **kwargs)


    def isbn13(self):
        """ '9780316769174' -> '978-0-31-676917-4' """
        return "{}-{}-{}-{}-{}".format(self.isbn[0:3], self.isbn[3:4],
                                       self.isbn[4:6], self.isbn[6:12],
                                       self.isbn[12:13])

    def __str__(self):
        return self.title

    class Meta:
        verbose_name = _("Book")
        verbose_name_plural = _("Books")
        ordering = ['-date_started', 'book_finished']


class Contributor(models.Model):
    """A contributor to a Book, e.g. author, editor, co-author."""
    first_names = models.CharField(max_length=50, unique=True,
                                   help_text="The contributor's first name or names.")
    last_names = models.CharField(max_length=50, unique=True,
                                  help_text="The contributor's last name or names.")

    def __str__(self):
        return "{} {}".format(self.first_names, self.last_names)


class BookContributor(models.Model):
    class ContributionRole(models.TextChoices):
        AUTHOR = "AUTHOR", "Author"
        CO_AUTHOR = "CO_AUTHOR", "Co-Author"
        EDITOR = "EDITOR", "Editor"

    book = models.ForeignKey(Book, on_delete=models.CASCADE)
    contributor = models.ForeignKey(Contributor, on_delete=models.CASCADE)
    role = models.CharField(verbose_name=_("The role this contributor had in the book."),
                            choices=ContributionRole.choices, max_length=20)

    def __str__(self):
        return "{} by {} ({})".format(self.book.title, self.contributor.last_names, self.role)


class Review(models.Model):
    rating = models.PositiveIntegerField(validators=[MaxValueValidator(5)], help_text="The rating for the book.")
    book = models.OneToOneField(Book, on_delete=models.CASCADE)
    content = models.TextField(help_text="The Review text.")
    date_created = models.DateTimeField(auto_now_add=True, 
                                        help_text="The date and time the review was created.")

    def __str__(self):
        return "{} Review".format(self.book)