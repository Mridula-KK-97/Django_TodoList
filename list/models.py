# list/models.py
from django.db import models
from datetime import date

class Task(models.Model):
    STATUS_CHOICES = [
        ('Pending', 'Pending'),
        ('Completed', 'Completed'),
    ]

    title = models.CharField(max_length=200)
    status = models.CharField(max_length=20, default='Pending')
    created_at = models.DateField(auto_now_add=True)
    due_date = models.DateField()

    def due_status(self):
        today = date.today()
        if self.due_date == today:
            return "Due Today"
        elif self.due_date < today:
            return "Overdue"
        else:
            return self.due_date.strftime("%Y-%m-%d")

    def __str__(self):
        return self.title
