from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, SiteConfiguration

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ('username', 'email', 'role')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remove 'admin' from the role dropdown to prevent public admin registration
        self.fields['role'].choices = [
            (k, v) for k, v in CustomUser.ROLE_CHOICES if k != 'admin'
        ]
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
        return user

class SiteConfigurationForm(forms.ModelForm):
    class Meta:
        model = SiteConfiguration
        fields = '__all__'
        widgets = {
            'admin_primary_color': forms.TextInput(attrs={'type': 'color'}),
            'admin_secondary_color': forms.TextInput(attrs={'type': 'color'}),
            'voter_primary_color': forms.TextInput(attrs={'type': 'color'}),
            'voter_secondary_color': forms.TextInput(attrs={'type': 'color'}),
            'candidate_primary_color': forms.TextInput(attrs={'type': 'color'}),
            'candidate_secondary_color': forms.TextInput(attrs={'type': 'color'}),
            'groq_api_key': forms.PasswordInput(render_value=True),
        }
