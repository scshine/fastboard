from django.conf.urls import patterns, include, url

from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'simpleboard.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^$', 'board.views.landing', name='landing'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^board/$', 'board.views.index', name='index'),
    url(r'^board/login$', 'django.contrib.auth.views.login', {'template_name': 'login.html'}, name='login'),
    url(r'^board/logout$', 'board.views.do_logout', name='logout'),
    url(r'^board/signup$', 'board.views.signup', name='signup'),
    url(r'^board/submit$', 'board.views.submit_board', name='submit_board'),
    url(r'^board/(?P<board_id>\d+)/$', 'board.views.board', name='board'),
    url(r'^board/(?P<board_id>\d+)/(?P<article_id>\d+)/$', 'board.views.article', name='article'),
    url(r'^board/(?P<board_id>\d+)/(?P<article_id>\d+)/delete$', 'board.views.delete_article', name='delete_article'),
    url(r'^board/(?P<board_id>\d+)/(?P<article_id>\d+)/update$', 'board.views.update_article', name='update_article'),
    url(r'^board/(?P<board_id>\d+)/(?P<article_id>\d+)/reply$', 'board.views.new_reply', name='new_reply'),
    url(r'^board/(?P<board_id>\d+)/new$', 'board.views.new_article', name='new_article'),
    url(r'^board/(?P<board_id>\d+)/submit$', 'board.views.submit_article', name='submit_article'),
    
    

)
