# counseling/models.py
from django.db import models
from accounts.models import CustomUser

class CounselingSession(models.Model):
    counselor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sessions_given')
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='sessions_received')
    session_date = models.DateTimeField()
    notes = models.TextField(blank=True)
    completed = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Session {self.id} - {self.counselor} with {self.user}"

# Run migrations after adding models
# python manage.py makemigrations
# python manage.py migrate