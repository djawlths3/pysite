from django.db import models

# Create your models here.
class Guestbook(models.Model):
    name = models.CharField(max_length=20)
    password = models.CharField(max_length=32)
    contents = models.TextField(null=False)
    writedate = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f'Guestbook({self.name},{self.contents})'