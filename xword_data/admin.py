from django.contrib import admin

from .models import Puzzle, Entry, Clue

admin.site.register(Puzzle)
admin.site.register(Entry)
admin.site.register(Clue)