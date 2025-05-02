
from django import forms
from django.contrib.auth.forms import UserCreationForm
from .models import CustomUser, UserProfile, CounselorProfile

class UserRegistrationForm(UserCreationForm):
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2']

class CounselorRegistrationForm(UserCreationForm):
    qualifications = forms.CharField(widget=forms.Textarea)
    specialization = forms.CharField(max_length=100)
    years_of_experience = forms.IntegerField()
    
    class Meta:
        model = CustomUser
        fields = ['email', 'first_name', 'last_name', 'password1', 'password2',
                  'qualifications', 'specialization', 'years_of_experience']
    
    def save(self, commit=True):
        user = super().save(commit=False)
        if commit:
            user.save()
            CounselorProfile.objects.create(
                user=user,
                qualifications=self.cleaned_data['qualifications'],
                specialization=self.cleaned_data['specialization'],
                years_of_experience=self.cleaned_data['years_of_experience']
            )
        return user