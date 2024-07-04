from django.db import models

# Create your models here.
from django.db import models

class BinInfo(models.Model):
    bin_number = models.CharField(max_length=6, unique=True)
    bank_name = models.CharField(max_length=255)

    def __str__(self):
        return f'{self.bin_number} - {self.bank_name}'
