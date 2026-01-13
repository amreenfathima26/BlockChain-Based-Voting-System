from django import forms
from .models import Election, Candidate

class ElectionForm(forms.ModelForm):
    class Meta:
        model = Election
        fields = ['title', 'description', 'start_date', 'end_date']
        widgets = {
            'start_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
            'end_date': forms.DateTimeInput(attrs={'type': 'datetime-local'}),
        }

class CandidateApplicationForm(forms.ModelForm):
    election = forms.ModelChoiceField(queryset=Election.objects.filter(is_active=True), empty_label="Select Election")
    
    class Meta:
        model = Candidate
        fields = ['election', 'party', 'symbol', 'manifesto']

class AdminCandidateForm(forms.ModelForm):
    # Admin can select any active election even if live
    election = forms.ModelChoiceField(queryset=Election.objects.all(), empty_label="Select Election")
    # Admin selects user to promote (ideally filter by those who aren't candidates yet, but all is fine for MVP)
    # We'll just show all users for simplicity or filter by role? Let's show all.
    
    class Meta:
        model = Candidate
        fields = ['user', 'election', 'party', 'symbol', 'manifesto']
