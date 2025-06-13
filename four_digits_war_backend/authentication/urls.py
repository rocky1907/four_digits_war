from django.urls import path
from .views import QuickLoginView

urlpatterns = [
    path('quick-login/', QuickLoginView.as_view(), name='quick_login')
]