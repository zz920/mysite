from django.db import models


class User(models.Model):
    """
    visitor info
    """

    user_ip = models.GenericIPAddressField()
    log_date = models.DateField(auto_now=True)

    def __str__(self):
        return "%s @ %s" % (self.user_ip, self.log_date)
