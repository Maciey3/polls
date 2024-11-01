from django.db import models
from django.contrib.auth.models import User


class Poll(models.Model):
    question = models.TextField()
    description = models.TextField(null=True, blank=True)
    made_by = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-updated', '-created']

    def __str__(self):
        return self.question

    @property
    def options(self):
        return (self.option_set.all())

    @property
    def user(self):
        return self.made_by

class Option(models.Model):
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    label = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"Option: {self.label}"


class Vote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    option = models.ForeignKey(Option, on_delete=models.CASCADE)
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.option.label

