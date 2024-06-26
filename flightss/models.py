from django.db import models

# Create your models here.

class Airline(models.Model):
    name = models.CharField(max_length = 255)
    iata_code = models.CharField(max_length = 3)
    icao_code = models.CharField(max_length = 4)
    
    def __str__(self):
        return self.name
    