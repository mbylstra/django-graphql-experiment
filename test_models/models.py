from django.db import models

# Create your models here.
from django.db.models import TextField, ForeignKey


class Address(models.Model):

    street = TextField()
    city = TextField()
    country = TextField()

class Person(models.Model):

    name = TextField()
    nickname = TextField()
    address = ForeignKey(Address)

    def __unicode__(self):
        return self.name
