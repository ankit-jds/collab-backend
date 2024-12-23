from django.db import models

class Document(models.Model):
    id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=100)
    content = models.TextField(default="")
    created_on = models.DateTimeField(auto_now_add=True)
    updated_on = models.DateTimeField(auto_now=True)

    def __str__(self):
        return self.name

    @property
    def created_on_strf(self):
        return self.created_on.strftime("%d/%m/%Y %H:%M:%S")

    @property
    def updated_on_strf(self):
        return self.updated_on.strftime("%d/%m/%Y %H:%M:%S")
