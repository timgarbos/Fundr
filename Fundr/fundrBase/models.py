from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='project_images/',blank=False)

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
	return u'%s is %s on %s' % (self.user, self.access, self.project)



class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project)
    
    
    #image

    def currentFund(self):
        value = 0
        for d in self.donation_set.all():
            value +=d.amount
        return value
        
    def averageFund(self):
        if self.donation_set.count()==0:
            return 0
        return self.currentFund()/self.donation_set.count()
       

        
    def activeStatus(self):
        #get latest status
        return self.featurestatusentry_set.all().order_by('-created')[0]
        
    def percentageFunded(self):
        return float((self.currentFund()/self.activeStatus().goal))*100
        
    def __unicode__(self):
	    return u'%s (%s)' % (self.name, self.project)


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
	return u'%s : %s' % (self.feature, self.status)


class Donation(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    feature = models.ForeignKey(Feature)
    amount = models.DecimalField(max_digits=20,decimal_places=4)
    user = models.ForeignKey(User)
    comment = models.TextField()
    #image

    def __unicode__(self):
	return u'%s : %s to %s' % (self.user, self.amount, self.feature)
	

	
from django.forms import ModelForm
	
#forms
class DonationForm(ModelForm):
    class Meta:
        model = Donation
        fields = ('amount', 'comment')


