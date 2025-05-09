from django.db import models

# Create your models here.

class NumberEntry(models.Model):
    """
    Model to store the numbers received from the third-party API
    """
    value = models.IntegerField()
    number_type = models.CharField(max_length=1)  # 'p', 'f', 'e', 'r'
    timestamp = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-timestamp']

    def __str__(self):
        return f"{self.value} ({self.number_type})"
