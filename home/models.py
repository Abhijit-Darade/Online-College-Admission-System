from django.db import models
from django.contrib.auth.models import User
from django.utils.timezone import now
from django.urls import reverse


class Application(models.Model):
    COURSES = (
        ('Computer Science Engineering', 'Computer Science Engineering'),
        ('Information Technology Engineering',
         'Information Technology Engineering'),
        ('Bio Medical Engineering',
         'Bio Medical Engineering'),
        ('Electronics Engineering', 'Electronics Engineering'),
    )

    STATUS = (
        ('Approved', 'Approved'),
        ('Pending', 'Pending'),
        ('Rejected', 'Rejected'),
    )

    user = models.OneToOneField(
        User, on_delete=models.CASCADE, blank=True, null=True)
    course = models.CharField(max_length=100, choices=COURSES)
    name = models.CharField(max_length=200)
    email = models.CharField(max_length=200)
    phone_no = models.CharField(max_length=200)
    address = models.TextField(max_length=200)
    student_profile = models.ImageField(upload_to="images/")
    ssc_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, null=True)
    ssc_marksheet = models.ImageField(upload_to="images/", null=True)
    ssc_passing_certificate = models.ImageField(upload_to="images/", null=True)
    ssc_leaving_certificate = models.ImageField(upload_to="images/", null=True)
    hsc_percentage = models.DecimalField(
        max_digits=4, decimal_places=2, null=True)
    hsc_marksheet = models.ImageField(upload_to="images/", null=True)
    hsc_passing_certificate = models.ImageField(upload_to="images/", null=True)
    hsc_leaving_certificate = models.ImageField(upload_to="images/", null=True)
    cet_percentile = models.DecimalField(
        max_digits=5, decimal_places=3, null=True)
    cet_scorecard = models.ImageField(upload_to="images/", null=True)
    jee_percentile = models.DecimalField(
        max_digits=5, decimal_places=3, null=True)
    jee_scorecard = models.ImageField(upload_to="images/", null=True)
    Application_Status = models.TextField(
        max_length=100, choices=STATUS, default="Pending")
    message = models.TextField(
        max_length=100, default="", null=True, blank=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('users')


class Notice(models.Model):
    title = models.CharField(max_length=200)

    def __str__(self):
        return self.title


class Detail(models.Model):
    title = models.ForeignKey(Notice, on_delete=models.CASCADE)
    notice = models.CharField(max_length=200)

    def __str__(self):
        return self.notice

class Person(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    address = models.TextField()
