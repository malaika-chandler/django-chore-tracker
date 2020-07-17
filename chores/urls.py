from django.conf.urls import url
from chores import views

app_name = 'chores'

urlpatterns = [
    url(r'^$', views.ChoreListView.as_view(), name='chore_list'),
    url(r'^chore/(?P<pk>\d+)$', views.ChoreDetailView.as_view(), name='chore_detail'),
    url(r'^chore/new/$', views.submit_new_chore, name='chore_new'),
    url(r'^chore/(?P<pk>\d+)/edit/$', views.edit_chore, name='chore_edit'),
    url(r'^chore/(?P<pk>\d+)/remove/$', views.ChoreDeleteView.as_view(), name='chore_remove'),
]
