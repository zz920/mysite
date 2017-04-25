from django.db import models
from datetime import datetime


class Tag(models.Model):

    """
    # Description: blog tag description.
    """

    text = models.CharField(max_length=16)

    def __str__(self):
        return "%s" % self.text

class MainPage(models.Model):

    """
    # Description: main page shown on the index page, consists of multiple
    # blog web page link and their short introduction.
    """

    visit_count = models.BigIntegerField()

    def getPages(self):
        return [(webpage.title, webpage.date, webpage.introduction, webpage.pk) for webpage in self.webpages.all().order_by('-pk')]

    def __str__(self):
        return "Home Page"

class WebPage(models.Model):

    """
    # Description: single web page consists of updated blog version with
    # comments.
    """

    introduction = models.CharField(max_length=255)
    mainpage = models.ForeignKey(MainPage, null=True, on_delete=models.SET_NULL, related_name='webpages')

    @property
    def title(self):
        if not self.blog_list.count(): return "None title"
        return self.blog_list.all().order_by('-mod_date')[0].title

    @property
    def date(self):
        if not self.blog_list.count(): return datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        return self.blog_list.all().order_by('-mod_date')[0].mod_date

    def __str__(self):
        return self.title


class Blog(models.Model):

    """
    # Description: basic blog page model.
    """

    title = models.CharField(max_length=30)
    mod_date = models.DateTimeField(auto_now=True)
    content = models.TextField()
    web_page = models.ForeignKey(WebPage, null=True, on_delete=models.SET_NULL, related_name='blog_list')

    tags = models.ManyToManyField(Tag)

    def __str__(self):
        return "%s @ %s" % (self.title, self.mod_date)


class Comment(models.Model):

    """
    # Description: web page comments.
    """

    user_ip = models.GenericIPAddressField()
    content = models.TextField()
    mod_date = models.DateTimeField(auto_now=True)
    web_page = models.ForeignKey(WebPage, null=True, on_delete=models.SET_NULL, related_name='n_comments')


class UserInfo(models.Model):

    """
    # Description: contain visitor's information, such as ip_address, date.
    """

    user_ip = models.GenericIPAddressField()
    log_date = models.DateField(auto_now=True)


    def __str__(self):
        return "%s @ %s" % (self.user_ip, self.log_date)
