from django.db import models
from .airport import Airport


class FlightSearch(models.Model):
    origin = models.ForeignKey(
        Airport,
        on_delete=models.PROTECT,
        related_name="searches",
    )

    departure_date = models.DateField()
    return_date = models.DateField(null=True, blank=True)
    max_price = models.DecimalField(
        max_digits=8,
        decimal_places=2,
        null=True,
        blank=True,
    )

    created_at = models.DateTimeField(auto_now_add=True)