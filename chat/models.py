
from django.db import models
from accounts.models import CustomUser

class ChatRoom(models.Model):
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='user_chatrooms')
    counselor = models.ForeignKey(CustomUser, on_delete=models.CASCADE, related_name='counselor_chatrooms')
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        unique_together = ('user', 'counselor')
    
    def __str__(self):
        return f"Chat between {self.user} and {self.counselor}"

class Message(models.Model):
    room = models.ForeignKey(ChatRoom, on_delete=models.CASCADE, related_name='messages')
    sender = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()
    timestamp = models.DateTimeField(auto_now_add=True)
    read = models.BooleanField(default=False)
    
    def __str__(self):
        return f"Message from {self.sender} in {self.room}"