from django.urls import path
from . import views

urlpatterns = [
    path('', views.requests_list_create, name='requests_list_create'),
    path('export/', views.export_requests, name='export_requests'),
    path('<uuid:request_id>/', views.request_detail_update, name='request_detail_update'),
]