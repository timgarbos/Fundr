from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    #image

    def __unicode__(self):
	return self.name

PROJECT_ACCESS_CHOICES = (
    ('A', 'Admin'),
    ('N', 'Normal'),

)

class ProjectAccess(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    access = models.CharField(max_length=1, choices=PROJECT_ACCESS_CHOICES )
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
    #image

    def __unicode__(self):
	return self.user + " -> "+ self.project


class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project)
    #image

    def __unicode__(self):
	return self.name


FEATURE_STATUS_OPTIONS = (
    ('P', 'In progress'),
    ('C', 'Created'),
    ('A', 'Accepted'),
    ('F', 'Funded'),
    ('V', 'Verified'),
    ('X', 'Canceled'),
)

class FeatureStatusEntry(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    feature = models.ForeignKey(Feature)
    goal = models.DecimalField(max_digits=20,decimal_places=4)
    status = models.CharField(max_length=1, choices=FEATURE_STATUS_OPTIONS)

    #image

    def __unicode__(self):
	return self.feature + " : "+ self.status


class Donation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    feature = models.ForeignKey(Feature)
    amount = models.DecimalField(max_digits=20,decimal_places=4)
    user = models.ForeignKey(User)
    #image

    def __unicode__(self):
	return self.user +" : " self.amount + " to " + self.feature
