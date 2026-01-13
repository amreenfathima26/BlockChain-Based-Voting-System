from django.db import models
from core.models import CustomUser

class Election(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    is_active = models.BooleanField(default=True)
    created_by = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.title

class Candidate(models.Model):
    election = models.ForeignKey(Election, on_delete=models.CASCADE, related_name='candidates')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, limit_choices_to={'role': 'candidate'})
    manifesto = models.TextField()
    party = models.CharField(max_length=100)
    symbol = models.CharField(max_length=10, default='👤') # Emoji or short char
    is_approved = models.BooleanField(default=False)
    
    def __str__(self):
        return f"{self.user.username} - {self.party}"

class Vote(models.Model):
    # This table tracks *who* voted to prevent double voting
    # The actual vote result is in the Blockchain
    election = models.ForeignKey(Election, on_delete=models.CASCADE)
    voter = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    timestamp = models.DateTimeField(auto_now_add=True)
    block_index = models.IntegerField(help_text="Reference to the block containing the vote")

    class Meta:
        unique_together = ('election', 'voter')
    
    def __str__(self):
        return f"{self.voter.username} voted in {self.election.title}"
