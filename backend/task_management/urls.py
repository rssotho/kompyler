from django.urls import path

from task_management import views


urlpatterns = [

    # Task
    path('get_task/', views.get_task, name = 'get_task'),
    path('edit_task/', views.edit_task, name = 'edit_task'),
    path('create_task/', views.create_task, name = 'create_task'),
    path('delete_task/', views.delete_task, name = 'delete_task'),
    path('get_all_tasks/', views.get_all_tasks, name = 'get_all_tasks'),

    # Team
    path('edit_team/', views.edit_team, name = 'edit_team'),
    path('view_team/', views.view_team, name = 'view_team'),
    path('create_team/', views.create_team, name = 'create_team'),
    path('delete_team/', views.delete_team, name = 'delete_team'),
    path('view_all_teams/', views.view_all_teams, name = 'view_all_teams'),
]