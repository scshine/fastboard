from django.db import models

class Board(models.Model):
	title = models.CharField('title', max_length=200)
	desc = models.CharField('description', max_length=1024)
	created_date = models.DateTimeField('written date', auto_now_add=True)
	
	def __unicode__(self):
		return self.title

class Article(models.Model):
	board = models.ForeignKey(Board)
	title = models.CharField('title', max_length=200)
	content = models.TextField('contents', default="")
	author = models.CharField('author username', max_length=200)
	written_date = models.DateTimeField('written date', auto_now_add=True)
	update_date = models.DateTimeField('update date', auto_now=True)

	def __unicode__(self):
		return "%s : %s" % (self.title, self.content)

class Reply(models.Model):
	article = models.ForeignKey(Article)
	content = models.TextField('reply')
	written_date = models.DateTimeField('written_date', auto_now_add=True)

	def __unicode__(self):
		return "Re: %s, %s" % (self.article.title, self.content)
