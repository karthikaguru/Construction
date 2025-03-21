from django.db import models
from django.contrib.auth.models import User
from django.conf import settings  # Import the settings module



class Client(models.Model):
    user = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    name = models.CharField(max_length=50, default='')
    phone_number = models.CharField(max_length=20)
    email = models.EmailField()
    site_location = models.CharField(max_length=200)
    site_name = models.CharField(max_length=100)
    project_start_date = models.DateField()
    project_end_date = models.DateField()
    project_duration = models.IntegerField(editable=False, null=True)  # Auto-calculated
    documents = models.FileField(upload_to='documents/', null=True, blank=True)

    def save(self, *args, **kwargs):
        self.project_duration = (self.project_end_date - self.project_start_date).days
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
class Project(models.Model):
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]

    client = models.ForeignKey(Client, on_delete=models.CASCADE, related_name='projects')
    name = models.CharField(max_length=100)
    budget = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    length = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Length (feet)")
    breadth = models.DecimalField(max_digits=10, decimal_places=2, null=True, blank=True, verbose_name="Breadth (feet)")
    total_land_area = models.DecimalField(max_digits=10, decimal_places=2, editable=False, null=True, verbose_name="Total Land Area (sq ft)")
     
    def save(self, *args, **kwargs):
        # Dynamically calculate total land area if length and breadth are provided
        if self.length and self.breadth:
            self.total_land_area = (self.length * self.breadth ).sq.ft
        else:
            self.total_land_area = None
        super().save(*args, **kwargs)
   
    def __str__(self):
        return self.name

    def update_status(self):
        """
        Dynamically updates the status of the project based on its related stages.
        """
        # Check related stages
        if self.stages.filter(status='in_progress').exists():
            self.status = 'in_progress'
        elif self.stages.filter(status='not_started').exists():
            self.status = 'not_started'
        elif self.stages.filter(status='on_hold').exists():
            self.status = 'on_hold'
        elif self.stages.filter(status='completed').count() == self.stages.count():
            self.status = 'completed'
        else:
            self.status = 'not_started'

        # Save the updated status
        self.save()



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
  
    STATUS_CHOICES = [
        ('not_started', 'Not Started'),
        ('in_progress', 'In Progress'),
        ('completed', 'Completed'),
        ('on_hold', 'On Hold'),
    ]
    project = models.ForeignKey(Project, on_delete=models.CASCADE, related_name='stages')
    name = models.CharField(max_length=100)
    due_date = models.DateField()
    start_date = models.DateField()
    end_date = models.DateField(null=True, blank=True)
    progress = models.IntegerField(default=0)  # Percentage progress
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='not_started')
    stage_type = models.CharField(max_length=50, choices=STAGE_CHOICES)
    def __str__(self):
        return f"{self.name} - {self.project.name}"

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)  # Save stage instance
        # Update project status
        self.project.update_status()

class Expense(models.Model):
    project = models.ForeignKey(Project, on_delete=models.CASCADE,related_name='expenses', verbose_name="Project")
    stage = models.ForeignKey(Stage, on_delete=models.SET_NULL, null=True, blank=True, verbose_name="Stage")
    description = models.TextField()
    amount_spent = models.DecimalField(max_digits=10, decimal_places=2, verbose_name="Amount Spent")
    date = models.DateField(verbose_name="Date")

    class Meta:
        ordering = ['date']
        verbose_name = "Expense"
        verbose_name_plural = "Expenses"

    def __str__(self):
        return f"{self.date} - {self.project.name} - {self.stage.stage_type if self.stage else 'No Stage'}"
