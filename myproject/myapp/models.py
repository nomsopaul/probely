from django.db import models

from django.db import models

class Finding(models.Model):
    id = models.AutoField(primary_key=True)
    target_id = models.IntegerField()
    definition_id = models.IntegerField()
    scans = models.IntegerField()
    url = models.URLField()
    path = models.CharField(max_length=255)
    method = models.CharField(max_length=255)
