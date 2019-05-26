from django.db import models
from ckeditor.fields import RichTextField

from .tag import Tag
from .mixin import HistoryMixin 


class WebPage(HistoryMixin, models.Model):
    """
    Web page consists of updated blog version with comments.
    """

    title = models.CharField(max_length=255)
    short_introduction = models.CharField(max_length=255)
    
    content = RichTextField()
    tags = models.ManyToManyField(Tag)
