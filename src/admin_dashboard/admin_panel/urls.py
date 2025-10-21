"""Admin panel URL configuration"""
from django.urls import path
from . import views

urlpatterns = [
    # Pages
    path('', views.dashboard_view, name='dashboard'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('logs/', views.logs_view, name='logs'),
    path('embeddings/', views.embeddings_view, name='embeddings'),

    # Bot Control APIs
    path('api/bot/start', views.api_bot_start, name='api_bot_start'),
    path('api/bot/stop', views.api_bot_stop, name='api_bot_stop'),
    path('api/bot/restart', views.api_bot_restart, name='api_bot_restart'),
    path('api/bot/status', views.api_bot_status, name='api_bot_status'),

    # Monitoring APIs
    path('api/stats', views.api_stats, name='api_stats'),
    path('api/uptime', views.api_uptime, name='api_uptime'),
    path('api/logs/stream', views.api_logs_stream, name='api_logs_stream'),
    path('api/logs/export', views.api_logs_export, name='api_logs_export'),

    # Embeddings APIs
    path('api/embeddings/stats', views.api_embeddings_stats, name='api_embeddings_stats'),
    path('api/embeddings/clear', views.api_embeddings_clear, name='api_embeddings_clear'),
    path('api/embeddings/process', views.api_embeddings_process, name='api_embeddings_process'),
]
