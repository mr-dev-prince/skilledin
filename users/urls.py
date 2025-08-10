from django.urls import path
from .views import ProfileView, RegisterView, LoginView, ProfileUpdateView, UserListView, UserDetailView

urlpatterns = [
    path('profile/', ProfileView.as_view(), name='profile'),
    path('profile/update/', ProfileUpdateView.as_view(), name='profile_update'),
    path('register/', RegisterView.as_view(), name='register'),
    path('login/', LoginView.as_view(), name='login'),
    path('get-users/', UserListView.as_view(), name='user-list'),
    path('get-user/<uuid:uuid>/', UserDetailView.as_view(), name='user-detail'),
]
