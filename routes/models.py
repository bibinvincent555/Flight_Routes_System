from django.db import models


class AirportRoute(models.Model):
    """
    Represents a node/stop in an ordered flight route.

    Fields:
    - airport_code: unique airport identifier (e.g., "JFK", "LAX")
    - position: integer ordering along the route (1-based, unique)
    - duration: a time-based metric for this airport node (in minutes)
                This could represent processing time, layover time, or any node-specific duration.
                The "shortest node" query finds the airport with the minimum duration value.
    
    Example:
        Position 1 (JFK, duration=120) - JFK has 120 min processing time
        Position 2 (LAX, duration=45)  - LAX has 45 min processing time (shortest)
        Position 3 (ORD, duration=90)  - ORD has 90 min processing time
    """
    airport_code = models.CharField(max_length=10, unique=True)
    position = models.IntegerField(db_index=True, unique=True)
    duration = models.PositiveIntegerField(help_text='Duration in minutes (node attribute)')

    class Meta:
        ordering = ['position']

    def __str__(self):
        return f"{self.airport_code} (pos {self.position}, {self.duration}m)"
