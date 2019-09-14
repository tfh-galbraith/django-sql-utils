from django.contrib.contenttypes.fields import GenericForeignKey, GenericRelation
from django.contrib.contenttypes.models import ContentType
from django.db import models
from django.db.models import CASCADE


# Simple parent-child model
class Parent(models.Model):
    name = models.CharField(max_length=32)


class Child(models.Model):
    name = models.CharField(max_length=32)
    parent = models.ForeignKey(Parent, on_delete=CASCADE)
    timestamp = models.DateTimeField()
    other_timestamp = models.DateTimeField(null=True)


# Books, Authors, Editors, there are more than 1 way Book/Author are m2m
# With publisher, there are multiple depths of traversal
class Author(models.Model):
    name = models.CharField(max_length=32)
    class Meta:
        ordering = ('name', )

class Publisher(models.Model):
    name = models.CharField(max_length=32)
    number = models.IntegerField()


class Book(models.Model):
    title = models.CharField(max_length=128)
    authors = models.ManyToManyField(Author, through='BookAuthor', related_name='authored_books')
    editors = models.ManyToManyField(Author, through='BookEditor', related_name='edited_books')
    publisher = models.ForeignKey(Publisher, on_delete=CASCADE, null=True)


class BookAuthor(models.Model):
    book = models.ForeignKey(Book, on_delete=CASCADE)
    author = models.ForeignKey(Author, on_delete=CASCADE)


class BookEditor(models.Model):
    book = models.ForeignKey(Book, on_delete=CASCADE)
    editor = models.ForeignKey(Author, on_delete=CASCADE)


class Catalog(models.Model):
    number = models.CharField(max_length=50)


class CatalogInfo(models.Model):
    catalog = models.ForeignKey(Catalog, on_delete=CASCADE)
    info = models.TextField()


class Package(models.Model):
    name = models.CharField(max_length=12)
    quantity = models.SmallIntegerField()
    catalog = models.ForeignKey(Catalog, on_delete=CASCADE)


class Purchase(models.Model):
    price = models.DecimalField(decimal_places=2, max_digits=10)
    pack = models.ForeignKey(Package, on_delete=CASCADE)


# This section deliberately has some weird names to make sure we correctly compute forward
# and backward joins

class Category(models.Model):
    name = models.CharField(max_length=12)


class Bit(models.Model):
    name = models.CharField(max_length=12)


# A collection of items. An Item can be in many Collections
# A collection is in a single category, or no categories (nullable)
class Collection(models.Model):
    name = models.CharField(max_length=12)
    the_category = models.ForeignKey(Category, null=True, on_delete=CASCADE)
    bits = models.ManyToManyField(Bit)


class Item(models.Model):
    name = models.CharField(max_length=12)
    collection_key = models.ManyToManyField(Collection, through='ItemCollectionM2M')


class ItemCollectionM2M(models.Model):
    thing = models.ForeignKey(Item, on_delete=CASCADE)
    collection_key = models.ForeignKey(Collection, on_delete=CASCADE)


# These models will make sure this works with GenericForeignKey/GenericRelation

class Dog(models.Model):
    name = models.CharField(max_length=12)


class Cat(models.Model):
    name = models.CharField(max_length=12)
    owner = GenericRelation('Owner', related_query_name='owner')


class Owner(models.Model):
    name = models.CharField(max_length=12)
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    pet = GenericForeignKey('content_type', 'object_id')


# These models will make sure this works with to_field ForeignKeys

class Brand(models.Model):
    name = models.CharField(max_length=12)
    company_id = models.IntegerField(unique=True)


class Product(models.Model):
    num_purchases = models.IntegerField()
    brand = models.ForeignKey(
        Brand,
        to_field='company_id',
        related_name='products',
        on_delete=models.CASCADE
    )

