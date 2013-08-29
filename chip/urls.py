from django.conf.urls import patterns, include, url

from chip import views

urlpatterns = patterns('',
    url(r'^$', views.index, name='index'),
    # ex: /chip/5/
    url(r'^(?P<chip_id>\d+)/$', views.detail, name='detail'),
    # ex: /chip/5/results/
    url(r'^(?P<chip_id>\d+)/results/$', views.results, name='results'),
    # ex: /chip/5/fetch/
    url(r'^fetch/(?P<fetch_url>.+)', views.fetch, name='vote'),
)