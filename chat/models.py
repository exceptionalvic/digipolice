from django.db import models

class InfoMessage(models.Model):
    username = models.CharField(max_length=255)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    ip_address = models.CharField(max_length=255, null=True, blank=True)
    location = models.CharField(max_length=255, null=True, blank=True)

    class Meta:
        db_table = "chat_message"
        ordering = ('-created_at',)
        
    # def save(self, *args, **kwargs):
    #     if self.username:
    #         self.username
        
    def __str__(self):
        return f'{self.username} - {self.created_at}'