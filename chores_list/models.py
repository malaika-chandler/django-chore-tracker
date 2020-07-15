from django.db import models
from django.urls import reverse
from datetime import timedelta


class Chore(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    repeats = models.BooleanField(default=True)
    count_repetitions = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    last_completed_by = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.DO_NOTHING)
    last_completed_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("chores_list:chore_detail", kwargs={'pk': self.pk})

    def mark_completed(self):
        pass


class ChoreInterval(models.Model):
    chore = models.ForeignKey(Chore, related_name='chore_intervals', on_delete=models.CASCADE)
    repeat_start = models.DateTimeField(auto_now_add=True)
    repeat_interval = models.IntegerField(blank=True, null=True)
    repeat_day_of_year = models.IntegerField(blank=True, null=True)
    repeat_day_of_month = models.IntegerField(blank=True, null=True)
    repeat_day_of_week = models.IntegerField(blank=True, null=True)
    repeat_hour_of_day = models.IntegerField(blank=True, null=True)
    repeat_minute_of_hour = models.IntegerField(blank=True, null=True)

    def __str__(self):
        starts = self.repeat_start.date().isoformat()
        td = timedelta(seconds=(self.repeat_interval))
        return "Starting {}, repeating every {}".format(starts, str(td))
