from django.db import models

# Create your models here.
from api.models import User

class Purchase(models.Model):
    user = models.ForeignKey(
        User, related_name='purchases', on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now=True)
    note = models.CharField(max_length=500)
    amount = models.DecimalField(decimal_places=2, max_digits=10)
    reference = models.CharField(max_length=400)

    class Meta:
        ordering = ['-timestamp']
