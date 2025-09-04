from django.db import models

class BusLocation(models.Model):
    lat = models.FloatField()
    lng = models.FloatField()
    timestamp = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.lat}, {self.lng}"  # Convert float to string and include lng
