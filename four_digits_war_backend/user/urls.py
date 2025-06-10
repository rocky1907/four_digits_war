from django.urls import path
from .views import UserListView, UserDetailView, UserMeView

urlpatterns = [
    path('users/', UserListView.as_view(), name='user-list'),  
    path('users/<int:pk>/', UserDetailView.as_view(), name='user-detail'),  
    path('users/me/', UserMeView.as_view(), name='user-me'),
]