from django.urls import path
from . import views

urlpatterns = [
    path('', views.get_users, name='get_users'),
    path('login/', views.login, name='login'),
    path('signup/', views.signup, name='signup'),
    path('edit-user/', views.edit_user, name='edit_user'),
    path('update-password/', views.update_password, name='update_password'),
    path('reset-password/', views.reset_password, name='reset_password'),
    path('delete-account/', views.delete_user, name='delete_own_account'),
    path('delete/<uuid:user_id>/', views.delete_user, name='delete_user_by_id'),
]