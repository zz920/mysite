from django.db import models
from ckeditor.fields import RichTextField

from .mixin import HistoryMixin
from .page import WebPage
from .user import User


class Comment(HistoryMixin, models.Model):
    """
    web page comments
    """
    content = RichTextField()
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    page = models.ForeignKey(WebPage, null=True, on_delete=models.CASCADE) 
