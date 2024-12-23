from django.db import models


class Operation(models.Model):
    id = models.AutoField(primary_key=True)
    document = models.ForeignKey(
        "Document", on_delete=models.DO_NOTHING, blank=False, null=False
    )
    operation_type = models.CharField(max_length=50, null=False, blank=False)
    position = models.IntegerField(null=False, blank=False)
    character = models.CharField(max_length=10)
    created_on = models.DateTimeField(auto_now_add=True)
    user_id = models.CharField(max_length=10, null=False, blank=False)
