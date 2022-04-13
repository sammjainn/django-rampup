from __future__ import unicode_literals
from email.policy import default

from django.db import models
from django.utils.encoding import smart_text as smart_unicode
from django.utils.translation import ugettext_lazy as _
from django.utils import timezone
from django.conf import settings


class Todo(models.Model):
    """
        Needed fields
        - user (fk to User Model - Use AUTH_USER_MODEL from django.conf.settings)
        - name (max_length=1000)
        - done (boolean with default been false)
        - date_created (with default of creation time)
        - date_completed (set it when done is marked true)

        Add string representation for this model with todos name.
    """

    user = models.ForeignKey(settings.AUTH_USER_MODEL,
                             on_delete=models.CASCADE)
    name = models.CharField(max_length=1000)
    done = models.BooleanField(default=False)
    date_created = models.DateTimeField(default=timezone.now)
    date_completed = models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.name

    def set_done(self):
        self.done = True
        self.date_completed = timezone.now()
        self.save()
