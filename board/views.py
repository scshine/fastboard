from board.models import Board, Article, Reply 
from django.http import HttpResponseRedirect, HttpResponse
from django.shortcuts import render, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout

def do_logout(request):
	logout(request)
	return HttpResponseRedirect('/')

def login(request):
	return render(request, 'login.html', {})

def signup_post(request):
	try:
		username = request.POST['username']
		password = request.POST['password']
		if username.strip() == '':
			raise ValidationError('Username must be provided', {
				'error_message': 'Username must be provided'
				})
		elif password.strip() == '':
			raise ValidationError('Password must be provided', {
				'error_message': 'Password must be provided'
				})
	except KeyError:
		return render(request, 'signup.html', {
				'error_message': 'Invalid access'
			})
	except ValidationError as e:
		return render(request, 'signup.html', e.errors)
	else:
		try:
			existing = User.objects.get(username=username)
			# an existing user found, redirect requester to signup page
			return render(request, 'signup.html', {
				'error_message': 'Provided username already exist'
				})
		except User.DoesNotExist as e:
			#expecting this error
			user = User.objects.create_user(username, 'youremail@example.com', password)
			user.save()
			return render(request, 'signup_success.html', {})

def signup(request):
	if request.method == 'GET':
		return signup_get(request)
	elif request.method == 'POST':
		return signup_post(request)
	else:
		return HttpResponseRedirect('/')

def signup_get(request):
	return render(request, 'signup.html', {})

def board(request, board_id):
	board = get_object_or_404(Board, id=board_id)
	articles = board.article_set.order_by('-written_date')
	return render(request, 'board.html', { 
		'board': board, 
		'articles': articles 
	})

def index(request):
	boards = Board.objects.order_by('-created_date')
	return render(request, 'index.html', { 'boards': boards })

@login_required
def delete_article(request, board_id, article_id):
	article = get_object_or_404(Article, id=article_id)
	article.delete()
	return HttpResponseRedirect('/board/%s' % (board_id,))

@login_required
def update_article(request, board_id, article_id):
	try:
		article_content = request.POST['article_content']
	except KeyError:
		context = { 
			'error_message': 'NO!'
		}
		return HttpResponseRedirect('/board/%s/%s' % (board_id, article_id,))
	else:
		article = get_object_or_404(Article, id=article_id)
		article.content = article_content
		article.save()
		return HttpResponseRedirect('/board/%s/%s' % (board_id, article_id,))

@login_required
def new_reply(request, board_id, article_id):
	article = get_object_or_404(Article, id=article_id)
	try:
		reply_content = request.POST['reply_content']
		if reply_content.strip() == '':
			raise ValidationError('Reply cannot be empty',{
				'article': article, 
				'reply_error': 'Reply cannot be empty.'
				})
	except KeyError:
		context = { 
			'article': article, 
			'error_message': 'NO!'
		}
		return render(request, 'article_detail.html', context)
	except ValidationError as e:
		return render(request, 'article_detail.html', e.errors)
	else:
		article.reply_set.create(content=reply_content)
		return HttpResponseRedirect('/board/%s/%s' % (board_id, article_id,))

@login_required
def submit_board(request):
	try:
		board_title = request.POST['board_title']
		board_desc = request.POST['board_desc']
	except KeyError:
		context = { 
			'error_message': 'NO!'
		}
		return render(request, 'index.html', context)
	else:
		board = Board(title=board_title, desc=board_desc)
		board.save()
		return HttpResponseRedirect('/board')

def article(request, board_id, article_id):
	article = get_object_or_404(Article, id=article_id)
	return render(request, 'article_detail.html', { 'article': article })

@login_required
def new_article(request, board_id):
	context = { 'board_id': board_id }
	return render(request, 'article_write.html', context)

@login_required
def submit_article(request, board_id):
	try:
		article_title = request.POST['article_title']
		article_content = request.POST['article_content']

		if article_title.strip() == '':
			raise ValidationError('Title cannot be empty', {
				'board_id': board_id,
				'error_message': 'Article title cannot be empty.' 
				})
		elif article_content.strip() == '':
			raise ValidationError('Content cannot be empty', {
				'board_id': board_id,
				'error_message': 'Article content cannot be empty.' 
				})
	except KeyError:
		context = { 
			'board_id': board_id,
			'error_message': 'Unauthorized access to the system.'
		}
		return render(request, 'article_write.html', context)
	except ValidationError as e:
		return render(request, 'article_write.html', e.errors)
	else:
		board = get_object_or_404(Board, id=board_id)
		board.article_set.create(title=article_title, content=article_content, author=request.user.username)
		return HttpResponseRedirect('/board/%s' % (board_id,))

def landing(request):
	return HttpResponseRedirect('/board')

class ValidationError(Exception):
    def __init__(self, message, errors):
        Exception.__init__(self, message)
        self.errors = errors