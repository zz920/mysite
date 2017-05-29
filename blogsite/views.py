from django.shortcuts import render
from django.http import HttpResponseRedirect
from django.http import StreamingHttpResponse

from blogsite import models
from markdown import markdown
from util.hackercrawler import getHackerNews
from datetime import datetime
import os
import wrapt
import logging


logger = logging.getLogger(__name__)

@wrapt.decorator
def analyzer(wrapped, instance, args, kwargs):

    """
    # count and analyze visitor information
    # save to the database
    """

    request = None
    if len(args): request = args[0]

    if request is not None:
        ip = request.META["REMOTE_ADDR"]
        try:
            models.UserInfo.objects.get_or_create(user_ip=ip)
        except Exception as e:
            logger.error(e)

    return wrapped(*args, **kwargs)



@analyzer
def homepage(request):

    """
    # Create home page with template index.html
    """
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    HACKER_FILE = os.path.join(BASE_DIR, "static", "data", "hacker_news.txt")
    SHOWN_PAGE_NUM = 5      #page number shown in the home page
    return_info = dict()

    try:
        mainpage = models.MainPage.objects.get(pk=1)

        return_info['visit_cnt'] = mainpage.visit_count
        return_info['pages'] = mainpage.getPages()[:SHOWN_PAGE_NUM]
        return_info['hackernews'] = getHackerNews(
            datetime.now().strftime("%Y-%m-%d %H-%M-%S"),
            HACKER_FILE
        )
    except Exception as e:
        logger.error(e)
        return render(request, 'index_static.html')

    return render(request, 'index.html', return_info)


@analyzer
def blogpage(request, pageid):

    """
    # Create blog page and comments
    """

    try:
        blog_page = models.WebPage.objects.get(pk=pageid).blog_list.all().reverse()[0]
        comments_list = models.WebPage.objects.get(pk=pageid).n_comments.all()
        tags = blog_page.tags.all()
    except Exception as e:
        logger.error(e)
        return render(request, '404.html')

    return_info = dict()
    return_info['page_id'] = pageid
    return_info['title'] = blog_page.title
    return_info['date'] = blog_page.mod_date
    return_info['body'] = blog_page.content
    return_info['tags'] = [t.text for t in tags]
    return_info['comments'] = [(cont.user_ip, cont.mod_date, cont.content) for cont in comments_list]

    return render(request, 'blog.html', return_info)


@analyzer
def aboutpage(request):

    """
    # Create self introduction page
    """

    ABOUTME_PAGE = 2        # introduction blog id
    text = models.Blog.objects.get(pk=ABOUTME_PAGE).content
    return render(request, 'about.html', {'body':text})


@analyzer
def searchpage(request, keyword):

    """
    # Search with keyword in content
    """
    pass


def resumedownload(request):

    """
    # Download link of my resume
    """
    
    BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

    def load_iter(filename, chunk_size=512):
        with open(filename, 'rb') as f:
            while True:
                c = f.read(chunk_size)
                if c:
                    yield c
                else:
                    break

    resumefile = os.path.join(BASE_DIR, 'static', 'resume.pdf') 

    response = StreamingHttpResponse(load_iter(resumefile))
    response['Content-Type'] = 'application/octet-stream'
    response['Content-Disposition'] = 'attachement;filename="{0}"'.format("resume.pdf")

    return response


def addcomment(request):

    """
    # add comment from website post
    """

    try:
        comment = request.GET['message']
        ip = request.META['REMOTE_ADDR']
        page_id = request.GET['page_id']
        page = models.WebPage.objects.get(pk=page_id) 
        models.Comment.objects.create(user_ip=ip,
                                      content=comment,
                                      web_page=page)
    except Exception as e:
        logger.error(e)
        return render(request, '404.html')
    
    return  HttpResponseRedirect(request.META.get('HTTP_REFERER'))


def notfound(request, path):
    return render(request, '404.html')
