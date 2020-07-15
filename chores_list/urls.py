from django.conf.urls import url
from chores_list import views

app_name = 'chores_list'

urlpatterns = [
    url(r'^$', views.ChoreListView.as_view(), name='chore_list'),
]
