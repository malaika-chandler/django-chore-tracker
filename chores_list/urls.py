from django.conf.urls import url
from chores_list import views

app_name = 'chores_list'

urlpatterns = [
    url(r'^$', views.ChoreListView.as_view(), name='chore_list'),
    url(r'^chore/(?P<pk>\d+)$', views.ChoreDetailView.as_view(), name='chore_detail'),
    url(r'^chore/new/$', views.ChoreCreateView.as_view(), name='chore_new'),
    url(r'^chore/(?P<pk>\d+)/edit/$', views.ChoreUpdateView.as_view(), name='chore_edit'),
    url(r'^chore/(?P<pk>\d+)/remove/$', views.ChoreDeleteView.as_view(), name='chore_remove'),
]
