from django.db import models


class Tag(models.Model):
    """
    Description: blog tag description
    """
    
    text = models.CharField(max_length=50)

    def __str__(self):
        return self.text
