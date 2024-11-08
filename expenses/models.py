from django.db import models
from django.utils.timezone import now
from django.contrib.auth.models import User

# Create your models here.

# models.ForeignKey is used to create a many-to-one relationship between two models. This means that each instance of one model can be associated with many instances of another model, while each instance of the second model can be associated with only one instance of the first.

#Example:
#Let's say we have two models: Expense and User. Each User can have multiple Expense instances, but each Expense is associated with only one User

class Expense(models.Model):
    amount = models.FloatField()
    date = models.DateField(default=now)
    description = models.TextField()
    owner = models.ForeignKey(to=User, on_delete=models.CASCADE)
    category = models.CharField(max_length=255)

    class Meta:
       #sorting
      ordering = ['-amount']

    def __str__(self):
        return self.category

class Category(models.Model):
    name = models.CharField(max_length=255)

    class Meta:
       verbose_name_plural = 'Categories'

    def __str__(self):
        return self.name