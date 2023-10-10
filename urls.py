# chat_app/urls.py

from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('groups/', views.group_list, name='group_list'),
    path('creategroup/', views.create_group, name='create_group'),
    path('joingroup/<int:group_id>/', views.join_group, name='join_group'),
    path('leavegroup/<int:group_id>/', views.leave_group, name='leave_group'),
    path('members/<int:group_id>/', views.group_members, name='members_group'),
    path('groupchat/<int:group_id>/', views.group_chat, name='group_chat'),
]
