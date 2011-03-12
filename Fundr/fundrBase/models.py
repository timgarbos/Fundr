from django.db import models
from django.contrib.auth.models import User

# Create your models here.


class Project(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    image = models.ImageField(upload_to='project_images/',blank=False)
    members = models.ManyToManyField(User, through='Membership')

    def get_active_features(self):
        set = self.feature_set.all()
        list = []
        for feature in set:
            if feature.activeStatus().status != 'R':
                list.append(feature)
        return list

    def get_requested_features(self):
        set = self.feature_set.all()
        list = []
        for feature in set:
            if feature.activeStatus().status == 'R':
                list.append(feature)
        return list

    def top_features(self):
        return self.feature_set.all()[0:3]

    def __unicode__(self):
        return self.name

PROJECT_ACCESS_CHOICES = (
    ('A', 'Admin'),
    ('N', 'Normal'),
)

class Membership(models.Model):
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    access = models.CharField(max_length=1, choices=PROJECT_ACCESS_CHOICES )
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)

    def __unicode__(self):
        return u'%s is %s on %s' % (self.user, self.access, self.project)


class Feature(models.Model):
    name = models.CharField(max_length=100)
    description = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    modified = models.DateTimeField(auto_now=True)
    project = models.ForeignKey(Project)
    user = models.ForeignKey(User)
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
        try:
            latest = self.featurestatusentry_set.all().order_by('-created')[0]
        except:
            print "No latest status entry could be found"
            pass
        return latest

    def percentageFunded(self):
        return float((self.currentFund()/self.activeStatus().goal))*100

    def __unicode__(self):
        return u'%s (%s)' % (self.name, self.project)


FEATURE_STATUS_OPTIONS = (
    ('P', 'In progress'),
    ('R', 'Requested'),
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

class ProjectForm(ModelForm):
    class Meta:
        model = Project
        fields = ('name', 'description', 'image')

class RequestFeatureForm(ModelForm):
    class Meta:
        model = Feature
        fields = ('name', 'description')

class FeatureStatusEntryForm(ModelForm):
    class Meta:
        model = FeatureStatusEntry
        fields = ('status', 'goal')

class EditFeatureForm(ModelForm):
    class Meta:
        model = Feature
        fields = ('name', 'description')
