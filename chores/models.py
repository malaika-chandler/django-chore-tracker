from django.db import models
from django.urls import reverse
from django.utils import timezone


class Chore(models.Model):
    name = models.CharField(max_length=256)
    description = models.TextField()
    repeats = models.BooleanField(default=True)
    datetime = models.DateTimeField(default=timezone.now)
    count_repetitions = models.PositiveIntegerField(default=0)
    completed = models.BooleanField(default=False)
    last_completed_by = models.ForeignKey('auth.User', blank=True, null=True, on_delete=models.DO_NOTHING)
    last_completed_on = models.DateTimeField(blank=True, null=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("chores:chore_detail", kwargs={'pk': self.pk})

    def mark_completed(self):
        pass


class ChoreInterval(models.Model):

    chore = models.ForeignKey(Chore, related_name='chore_intervals', on_delete=models.CASCADE)

    class IntervalChoice(models.TextChoices):
        DAILY = 'daily'
        WEEKLY = 'weekly'
        WEEK_DAILY = 'week daily'
        MONTHLY = 'monthly'
        YEARLY = 'yearly'
        CUSTOM = 'custom'

    repeat_start = models.DateTimeField(default=timezone.now)
    repeat_interval = models.CharField(choices=IntervalChoice.choices, max_length=10, default=IntervalChoice.DAILY)
    repeat_custom_interval = models.IntegerField(blank=True, null=True)

    def __str__(self):
        if self.repeat_interval != ChoreInterval.IntervalChoice.CUSTOM:
            interval = self.repeat_interval
        else:
            interval = 'every {} seconds'.format(self.repeat_custom_interval)

        return "Repeats {}".format(interval)


class ChoreInstance(models.Model):
    chore = models.ForeignKey(Chore, related_name='instances', on_delete=models.CASCADE)
    interval = models.ForeignKey(ChoreInterval, related_name='instances', null=True, on_delete=models.SET_NULL)
    datetime = models.DateTimeField()
    done = models.BooleanField(default=False)

    unique_together = ['chore', 'interval', 'datetime']

    @property
    def is_past_due(self):
        return timezone.now() > self.datetime

    def __str__(self):
        return "{} on {}".format(self.chore, self.datetime)
