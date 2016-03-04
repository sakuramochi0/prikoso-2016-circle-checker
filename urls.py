try:
    from django.conf.urls import *
except ImportError:  # django < 1.4
    from django.conf.urls.defaults import *

urlpatterns = patterns(
    '',
    url(r'^$', 'prikoso_2016_circle_checker.views.index', name='index'),
    url(r'^(?P<page>\d+)/$', 'prikoso_2016_circle_checker.views.index', name='index'),
    url(r'^(?P<page>\d+)/(?P<edit>edit)/$', 'prikoso_2016_circle_checker.views.index', name='index'),
    url(r'^disable/$', 'prikoso_2016_circle_checker.views.disable', name='disable'),
    url(r'^enable/$', 'prikoso_2016_circle_checker.views.enable', name='enable'),
    url(r'^pin/$', 'prikoso_2016_circle_checker.views.pin', name='pin'),
    url(r'^unpin/$', 'prikoso_2016_circle_checker.views.unpin', name='unpin'),
)
