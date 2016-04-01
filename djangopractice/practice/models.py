from django.db import models
from django.utils import timezone
from ckeditor.fields import RichTextField

class Publisher(models.Model):
    name = models.CharField(max_length=30)
    address = models.CharField(max_length=50)
    city = models.CharField(max_length=60)
    state_province = models.CharField(max_length=30)
    country = models.CharField(max_length=50)
    website = models.URLField()

    class Meta:
        ordering = ["-name"]

    def __str__(self):
        return self.name

class Author(models.Model):
    SAL_LIST = (
        ('Mr', 'Mr'),
        ('Miss', 'Miss'),
        ('Mrs', 'Mrs'),
    )
    salutation = models.CharField(max_length=10, choices=SAL_LIST)
    name = models.CharField(max_length=200)
    email = models.EmailField()
    headshot = models.ImageField(upload_to='author_headshots')

    def __str__(self):
        return self.name

class Book(models.Model):
    title = models.CharField(max_length=100)
    authors = models.ManyToManyField('Author')
    publisher = models.ForeignKey(Publisher, on_delete=models.CASCADE)
    publication_date = models.DateField()

    def __str__(self):
        return self.title


class Post(models.Model):
    author = models.ForeignKey('auth.User')
    title = models.CharField(max_length=200)
    text = RichTextField()
    created_date = models.DateTimeField(
            default=timezone.now)
    published_date = models.DateTimeField(
            blank=True, null=True)

    def publish(self):
        self.published_date = timezone.now()
        self.save()

    def __str__(self):
        return self.title

class Project(models.Model):
    name = models.CharField(max_length=200)

    def __str__(self):
        return self.name

class API(models.Model):
    METHOD_LIST = (
        ('GET', 'GET'),
        ('POST', 'POST'),
    )
    STATUS_LIST = (
        ('200', '200'),
        ('404', '404'),
        ('301', '301'),
        ('401', '401'),
    )
    CONTENT_LIST = (
        ('application/json', 'application/json'),
        ('application/xml', 'application/xml'),
        ('text/json', 'text/json'),
        ('text/xml', 'text/xml'),
        ('raw', 'raw'),
    )

    path = models.CharField(max_length=50, help_text="API Path")
    method = models.CharField(max_length=10, choices=METHOD_LIST, help_text="Response Method")
    res_status = models.CharField(max_length=10, choices=STATUS_LIST, help_text="Response Status")
    content_type = models.CharField(max_length=50, choices=CONTENT_LIST)
    response_body = RichTextField()
    response_delay = models.CharField(max_length=20,blank=True,default="0", help_text="Response Delay In Seconds")
    project = models.ForeignKey(Project, on_delete=models.CASCADE)

    def __str__(self):
        return self.path
