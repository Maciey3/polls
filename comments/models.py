from django.db import models
from django.contrib.auth.models import User
from base.models import Poll


class Comment(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    poll = models.ForeignKey(Poll, on_delete=models.CASCADE)
    text = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    deleted = models.DateTimeField(null=True, blank=True)

    @property
    def votes(self):
        return self.commentvote_set.all()

    @property
    def sum_of_votes(self):
        return sum(1 if vote.vote else -1 for vote in self.votes)



class CommentVote(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    comment = models.ForeignKey(Comment, on_delete=models.CASCADE)
    vote = models.BooleanField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)

