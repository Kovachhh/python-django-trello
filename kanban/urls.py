from django.urls import path
from . import views

app_name = 'kanban'

urlpatterns = [
    path('', views.board_list, name='board_list'),
    path('board/add/', views.add_board, name='add_board'),
    path('board/<int:board_id>/edit/', views.edit_board, name='edit_board'),
    path('board/<int:board_id>/delete/', views.delete_board, name='delete_board'),
    path('board/<int:board_id>/', views.board_detail, name='board_detail'),
    path('board/<int:board_id>/add_column/', views.add_column, name='add_column'),
    path('column/<int:column_id>/edit/', views.edit_column, name='edit_column'),
    path('column/<int:column_id>/delete/', views.delete_column, name='delete_column'),
    path('column/<int:column_id>/add_task/', views.add_task, name='add_task'),
    path('task/<int:task_id>/edit/', views.edit_task, name='edit_task'),
    path('task/<int:task_id>/delete/', views.delete_task, name='delete_task'),
    path('task/<int:task_id>/details/', views.task_detail, name='task_detail'),
    path('move-task/', views.move_task, name='move_task'),
]
