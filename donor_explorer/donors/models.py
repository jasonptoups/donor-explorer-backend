from django.db import models
from django.contrib.auth.models import User


class SavedDonor(models.Model):
    first_name = models.CharField(max_length=100)
    last_name = models.CharField(max_length=100)
    city = models.CharField(max_length=100)
    state = models.CharField(max_length=3)
    employer = models.CharField(max_length=100)
    occupation = models.CharField(max_length=100)
    average_donation = models.IntegerField()
    max_donation = models.IntegerField()
    mode_donation = models.IntegerField()
    total_donations = models.IntegerField()
    percent_dem = models.CharField(max_length=50, null=True, blank=True)
    user = models.ForeignKey(
          User,
          on_delete=models.CASCADE,
          related_name='donors',
          null=True,
          blank=True
    )

    def __str__(self):
        return self.last_name
