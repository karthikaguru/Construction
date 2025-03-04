from django.db import models
from django.contrib.auth.models import User

class Client(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    site_location = models.CharField(max_length=200)
    site_name = models.CharField(max_length=100)
    project_start_date = models.DateField()
    project_end_date = models.DateField()
    project_duration = models.IntegerField(editable=False)  # Auto-calculated
    project_budget = models.DecimalField(max_digits=10, decimal_places=2)
    documents = models.FileField(upload_to='documents/', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.project_duration = (self.project_end_date - self.project_start_date).days
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

class Project(models.Model):
    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()

    def __str__(self):
        return self.name



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
    start_date = models.DateField()  # Ensure this field is defined
    end_date = models.DateField() 
    stage_type = models.CharField(max_length=50, choices=STAGE_CHOICES)

class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE)
    description = models.CharField(max_length=200)
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2)
    date = models.DateField()

    def __str__(self):
        return self.description


