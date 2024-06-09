import os
from django.db import models

# Create your models here.

class UploadedFile(models.Model):
    file = models.FileField(upload_to='static/upload_files/')
    uploaded_at = models.DateTimeField(auto_now_add=True) 
    
    
    def fileName(self):
        return os.path.basename(self.file.name)
    def __str__(self):
        return str(self.id) + "__" + self.fileName