from django.db import models
from django.contrib.auth.models import User
from django.urls import reverse
from autoslug import AutoSlugField

# Create your models here.


class fb_user_pages(models.Model):
    page_id = models.CharField(blank=True, max_length=50)
    page_name = models.CharField(blank=True, max_length=50)
    slug = AutoSlugField(populate_from="page_name")
    page_access_token = models.CharField(blank=True, max_length=5000)

    def __str__(self):
        return self.page_name


class fb_users(models.Model):
    user_id = models.CharField(blank=True, max_length=50)
    user_name = models.CharField(blank=True, max_length=50)
    user_access_token = models.CharField(blank=True, max_length=2000)
    pages = models.ManyToManyField(fb_user_pages)

    def __str__(self):
        return self.user_name
        
class UserType(models.Model):
    id = models.AutoField(primary_key=True)
    user_type = models.CharField(max_length= 15)
    user = models.ForeignKey(User , on_delete=models.CASCADE)

    def __str__(self):
        return "%s %s" % (self.user, self.user_type)

class SchduleDemo(models.Model):
    id = models.AutoField(primary_key=True)
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    DealershipName = models.CharField(max_length=100)
    Emailaddress = models.CharField(max_length=100)
    PhoneNo = models.CharField(max_length=100)
    help = models.CharField(max_length=100)
    Question = models.CharField(max_length=100)
    def __str__(self):
        return "%s" % (self.id)


class addlogo(models.Model):
    id = models.AutoField(primary_key=True)
    logo = models.FileField(upload_to ='logo/',null=True)
    def __str__(self):
        return "%s" % (self.id)

class startegy(models.Model):
    id = models.AutoField(primary_key=True)
    attachment = models.FileField(upload_to ='attachment/',null=True)
    note = models.CharField(max_length=100)
    def __str__(self):
        return "%s" % (self.id)
class startegy1(models.Model):
    id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User , on_delete=models.CASCADE)
    comment = models.CharField(max_length=100)
    date = models.DateField()
    def __str__(self):
        return "%s" % (self.id)

class content(models.Model):
    id = models.AutoField(primary_key=True)
    video = models.FileField(upload_to ='videos/',null=True)
    tag = models.CharField(max_length=100)
    def __str__(self):
        return "%s" % (self.id)

class billingtable(models.Model):
    id = models.AutoField(primary_key=True)
    invoice = models.FileField(upload_to ='invoice/',null=True)
    def __str__(self):
        return "%s" % (self.id)

class Event(models.Model):
    role=(
        ('Schedule video','Schedule video'),
        ('Posted video','Posted video'),
        ('Other','Other'),
    )
    title = models.CharField(max_length=200 , choices=role)
    description = models.TextField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField()
   
    @property
    def get_html_url(self):
        url = reverse('event_edit', args=(self.id,))
        if self.title == 'Other':
             return f'<a href="{url}" class=btn1>ddd</a>'
        if self.title == 'Posted video':
            
             return f'<a href="{url}" class=btn2 >ddd </a>'
        if self.title == 'Schedule video':
            
             return f'<a href="{url}" class=btn3>ddd</a>'