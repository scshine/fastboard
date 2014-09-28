from django.contrib import admin
from board.models import Board, Article, Reply 

# Register your models here.
admin.site.register(Board)
admin.site.register(Article)
admin.site.register(Reply)