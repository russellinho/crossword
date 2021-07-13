from django.db import models


class Puzzle(models.Model):
    title = models.CharField(max_length=255, blank=True)
    date = models.DateTimeField('date published', blank=False, null=False)
    byline = models.CharField(max_length=255, blank=False)
    publisher = models.CharField(max_length=12, blank=False)

class Entry(models.Model):
    entry_text = models.CharField(max_length=50, blank=False, unique=True)

class Clue(models.Model):
    entry = models.ForeignKey(Entry, on_delete=models.CASCADE)
    puzzle = models.ForeignKey(Puzzle, on_delete=models.CASCADE)
    clue_text = models.CharField(max_length=512, blank=False)
    theme = models.BooleanField(default=False)
