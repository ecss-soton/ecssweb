from django.db import models


class Event(models.Model):
    fb_id = models.CharField(max_length=20, unique=True)
    name = models.CharField(max_length=100)
    location = models.CharField(max_length=100)
    cover = models.URLField()
    start_time = models.DateTimeField()
    end_time = models.DateTimeField(null=True)

    def __str__(self):
        return 'name: {},fb_id: {}'.format(self.name, self.fb_id)
