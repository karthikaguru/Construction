from django.db import models
from django.contrib.auth.models import User


class Client(models.Model):
    first_name = models.CharField(max_length=100,null=True,blank=True)
    last_name = models.CharField(max_length=100,null=True,blank=True)
    phone_number = models.IntegerField()
    email = models.EmailField(max_length=155)
    site_location = models.CharField(max_length=100)
    site_name = models.CharField(max_length=100)
    user = models.ForeignKey(User, on_delete=models.CASCADE)

class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    start_date = models.DateField()
    end_date = models.DateField()
    project_budget = models.DecimalField(max_digits=10, decimal_places=2)
    documents = models.FileField(upload_to='documents/', null=True, blank=True)
    
    @property
    def project_duration(self):
       return (self.end_date - self.start_date).days

class Stage(models.Model):
    STAGE_CHOICES = [
        ('ceiling', 'Ceiling'),
        ('flooring', 'Flooring'),
        ('plumbing', 'Plumbing'),
        ('painting', 'Painting'),
        ('foundation', 'Foundation'),
        ('framing', 'Framing'),
        ('electrical', 'Electrical'),
        ('hvac', 'HVAC'),
        ('roofing', 'Roofing'),
        ('drywall', 'Drywall'),
        ('insulation', 'Insulation'),
        ('siding', 'Siding'),
        ('windows', 'Windows'),
        ('doors', 'Doors'),
        ('landscaping', 'Landscaping'),
        ('finishing', 'Finishing'),
        ('furniture_installation', 'Furniture Installation'),
        ('final_touchups', 'Final Touch-ups')
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    due_date = models.DateField()
    completed = models.BooleanField(default=False)
    progress = models.IntegerField(default=0)
    stage_type = models.CharField(max_length=50, choices=STAGE_CHOICES)

class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    item = models.CharField(max_length=100)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

class Milestone(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField()
    due_date = models.DateField()
    status = models.IntegerField()

class Upload(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    file = models.FileField(upload_to='uploads/')
    upload_type = models.CharField(max_length=50)
 

