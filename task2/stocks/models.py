from django.db import models
from django.utils import timezone

class StockPrice(models.Model):
    ticker = models.CharField(max_length=20)
    price = models.FloatField()
    last_updated_at = models.DateTimeField()
    retrieved_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-last_updated_at']
        indexes = [
            models.Index(fields=['ticker', 'last_updated_at']),
        ]

    def __str__(self):
        return f"{self.ticker}: {self.price} at {self.last_updated_at}"
