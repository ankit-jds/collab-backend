from django.db import models


class Snapshot(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(
        "Document", on_delete=models.DO_NOTHING, blank=False, null=False
    )
    content = models.TextField(default="")
    created_on = models.DateTimeField(auto_now_add=True)
    upto_operation_id = models.IntegerField(blank=False, null=False)
    active = models.BooleanField(default=False)
