
# Create your models here.
from django.db import models

class Employee(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    gender = models.CharField(max_length=10)
    age = models.IntegerField()
    address = models.CharField(max_length=255)
    contact = models.CharField(max_length=20)
    department = models.CharField(max_length=100)
    employment_date = models.DateField()
    nationality = models.CharField(max_length=100)
    marital_status = models.CharField(max_length=10)

class Internship(models.Model):
    title = models.CharField(max_length=255)
    description = models.TextField()
    start_date = models.DateField()
    end_date = models.DateField()
    def __str__(self):
        return self.title
class Department(models.Model):
    name = models.CharField(max_length=100)
    manager = models.CharField(max_length=100)
    established_date = models.DateField()

    def __str__(self):
        return self.name
    
class Event(models.Model):
    title = models.CharField(max_length=255)
    date = models.DateField()
    location = models.CharField(max_length=255)
    description = models.TextField()

    def __str__(self):
        return self.title
    
class EmployeeFile(models.Model):
    content = models.TextField()
