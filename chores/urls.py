from django.urls import path
from chores import views

app_name = 'chores'

urlpatterns = [
    path('', views.ChoreInstanceListView.as_view(), name='chore_list'),
    path('all/', views.AllChoreListView.as_view(), name='total_chore_list'),
    path('completed/', views.CompletedChoreListView.as_view(), name='completed_chore_list'),
    path('completed-instances/', views.CompletedChoreInstanceListView.as_view(), name='completed_chore_instance_list'),
    path('overdue/', views.AllChoreListView.as_view(), name='overdue_chore_list'),
    path('chore/<int:pk>', views.ChoreDetailView.as_view(), name='chore_detail'),
    path('chore/<int:pk>/mark-complete/', views.mark_chore_complete, name='mark_chore_complete'),
    path('chore/new/', views.submit_new_chore, name='chore_new'),
    path('chore/<int:pk>/edit/', views.edit_chore, name='chore_edit'),
    path('chore/<int:pk>/remove/', views.ChoreDeleteView.as_view(), name='chore_remove'),
    # path('instance/<int:pk>/edit/', views.mark_chore_complete, name='chore_instance_edit'),
    path('instance/<int:pk>/remove/', views.delete_chore_instance, name='remove_chore_instance'),
    path('instance/<int:pk>/mark-complete/', views.mark_chore_instance_complete, name='mark_chore_instance_complete'),
]
