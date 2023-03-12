from django.db import models
from django.contrib.auth.models import User, ContentType
from django.contrib.contenttypes.fields import GenericForeignKey
from django.core import validators
from django.core.exceptions import ValidationError, NON_FIELD_ERRORS


# python manage.py shell_plus --print-sql

class Bb(models.Model):
    KINDS = (
        ('Buy-Sell', (
            ('b', 'buy'),
            ('s', 'sell'),
        )),
        ('Exchange', (
            ('e', 'exchange'),
        ))
    )
    title = models.CharField(max_length=50, verbose_name='Merchandise')
    content = models.TextField(null=True, blank=True, verbose_name='Description')
    price = models.FloatField(null=True, blank=True, verbose_name='Price')
    published = models.DateTimeField(auto_now_add=True, db_index=True, verbose_name='Published')
    rubric = models.ForeignKey('Rubric', null=True, on_delete=models.PROTECT, verbose_name='Rubric', related_name='bb')
    kind = models.CharField(max_length=2, choices=KINDS, default='s', null=True)

    class Meta:
        verbose_name_plural = 'Ads'
        verbose_name = 'Ad'
        ordering = ['-published']


class Rubric(models.Model):
    name = models.CharField(max_length=20, db_index=True, verbose_name='Name', unique=True)

    def __str__(self):
        return self.name

    class Meta:
        verbose_name_plural = 'Rubrics'
        verbose_name = 'Rubric'
        ordering = ['name']


class Book(models.Model):
    name = models.CharField(max_length=30, db_index=True, verbose_name='Book name',
                            validators=[validators.MinLengthValidator(5)],
                            error_messages={'invalid': 'Wrong name, you need more signs'})
    pages = models.IntegerField(null=False, blank=False)
    price = models.FloatField(null=True, blank=True)
    author = models.ForeignKey('Author', null=False, on_delete=models.PROTECT)

    def get_absolute_url(self):
        return '/bboard/book/%s/' % self.pk

    def clean(self):
        errors = {}
        if self.price and self.price < 0:
            errors['price'] = ValidationError('Enter not negative price')
        if self.pages and self.pages < 0:
            errors['pages'] = ValidationError('Enter not negative pages')
        if self.price + self.pages != 100:
            errors[NON_FIELD_ERRORS] = 'Error model, you need that page + price equals 100'
        if errors:
            raise ValidationError(errors)

    class Meta:
        order_with_respect_to = 'author'


class Author(models.Model):
    first_name = models.CharField(max_length=16, db_index=True, verbose_name='First Name',
                                  validators=[validators.RegexValidator(regex='^.{4,}$')],
                                  error_messages={'invalid': 'Wrong name, you need more signs'})
    last_name = models.CharField(max_length=24, db_index=True, verbose_name='Last Name')

    def __str__(self):
        return f'{self.last_name} {self.first_name}'


class UserInfo(models.Model):
    first_name = models.CharField(max_length=16, db_index=True, verbose_name='First Name')
    last_name = models.CharField(max_length=24, db_index=True, verbose_name='Last Name')
    add_info = models.OneToOneField('UserAddInfo', on_delete=models.CASCADE, default=None, null=True)
    words = models.ManyToManyField('Word', related_name='users')


class UserAddInfo(models.Model):
    city = models.CharField(max_length=24, db_index=True, verbose_name='Address', null=None)
    old = models.IntegerField(null=True, blank=False)
    birthday = models.DateField(null=True, blank=False)

    def __str__(self):
        return f'{self.old} years old. {self.city} {self.birthday}'


class Word(models.Model):
    eng_word = models.CharField(max_length=24, db_index=True, null=False)
    rus_word = models.CharField(max_length=24, db_index=True, null=True)

    def __str__(self):
        return f'{self.eng_word} {self.rus_word}'


class Movie(models.Model):
    name = models.CharField(max_length=24, db_index=True, null=False)
    actors = models.ManyToManyField('Actor')


class Actor(models.Model):
    name = models.CharField(max_length=16, db_index=True, null=False)


# MANY-TO-MANY WITH ADDITIONAL PARAMETERS
class Spare(models.Model):
    name = models.CharField(max_length=40)


class Machine(models.Model):
    name = models.CharField(max_length=30)
    spares = models.ManyToManyField(Spare, through='Kit', through_fields=('machine', 'spare'))


class Kit(models.Model):
    machine = models.ForeignKey(Machine, on_delete=models.CASCADE)
    spare = models.ForeignKey(Spare, on_delete=models.CASCADE)
    count = models.IntegerField()


# Create Model for Notes
class Note(models.Model):
    content = models.TextField()
    content_type = models.ForeignKey(ContentType, on_delete=models.CASCADE)
    object_id = models.PositiveIntegerField()
    content_object = GenericForeignKey(ct_field='content_type', fk_field='object_id')
