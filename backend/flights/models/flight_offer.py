from django.db import models
from .airport import Airport
from .flight_search import FlightSearch


class FlightOffer(models.Model):
    search = models.ForeignKey(
        FlightSearch,
        on_delete=models.CASCADE,
        related_name="offers",
    )

    origin = models.ForeignKey(
        Airport,
        on_delete=models.PROTECT,
        related_name="origin_offers",
    )

    destination = models.ForeignKey(
        Airport,
        on_delete=models.PROTECT,
        related_name="destination_offers",
    )

    airline = models.CharField(max_length=100)
    price = models.DecimalField(max_digits=8, decimal_places=2)