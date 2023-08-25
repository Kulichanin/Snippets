from django.db import models
from django.contrib.auth.models import User


LANGS = (
    ('py', "Python"),
    ('js', "JavaScript"),
    ('cpp', "C++")
)

class Snippet(models.Model):
    class Meta:
        ordering = ["name", "lang"]

    name = models.CharField(max_length=100)
    lang = models.CharField(max_length=30, choices=LANGS)
    code = models.TextField(max_length=5000)
    creation_date = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(to=User, on_delete=models.CASCADE, blank=True, null=True)
    public = models.BooleanField(default=True)  # True - public, False - private
    
    # В Админке используется метод __str__()
    def __str__(self):
        return f'Snippet({self.id}, {self.name})'

    def __repr__(self):
        return f'Snippet({self.id}, {self.name}, {self.lang}, {self.user})'
