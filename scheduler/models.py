from django.db import models

class ProcessHistory(models.Model):
    arrival = models.CharField(max_length=100)
    burst = models.CharField(max_length=100)
    quantum = models.IntegerField()

    fcfs_avg = models.FloatField()
    sjf_avg = models.FloatField()
    rr_avg = models.FloatField()

    best_algo = models.CharField(max_length=50)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.best_algo