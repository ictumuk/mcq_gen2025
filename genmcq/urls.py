from django.urls import path
from . import views
from .room_views_pkg import room_views, room_api

urlpatterns = [
    # Main pages
    path('', views.home, name='home'),
    path('generate-mcq/', views.generate_mcq, name='generate-mcq'),
    
    # Authentication
    path('register/', views.register_view, name='register'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    
    # User profile
    path('profile/', views.profile_view, name='profile'),
    path('dashboard/', views.dashboard_view, name='dashboard'),
    
    # API endpoints for question management
    path('api/questions/', views.api_get_questions, name='api-get-questions'),
    path('api/questions/create/', views.api_create_question, name='api-create-question'),
    path('api/questions/<uuid:question_id>/update/', views.api_update_question, name='api-update-question'),
    path('api/questions/<uuid:question_id>/delete/', views.api_delete_question, name='api-delete-question'),
    path('api/questions/clear-all/', views.api_clear_all_questions, name='api-clear-all-questions'),
    path('api/subjects/list/', views.api_get_subjects_list, name='api-get-subjects-list'),
    path('api/subjects/history/', views.api_get_subjects_history, name='api-get-subjects-history'),
    path('api/subjects/<uuid:subject_id>/delete/', views.api_delete_subject, name='api-delete-subject'),
    
    # Generation endpoint
    path('api/generate-mcq/', views.api_generate_mcq, name='api-generate-mcq'),
    
    # Source file upload
    path('api/source/upload/', views.api_upload_source, name='api-upload-source'),
    
    # ===== Chat Room URLs =====
    # Room page views
    path('rooms/', room_views.room_list, name='room-list'),
    path('rooms/create/', room_views.room_create, name='room-create'),
    path('rooms/<uuid:room_id>/', room_views.room_chat, name='room-chat'),
    path('rooms/<uuid:room_id>/join/', room_views.room_join, name='room-join'),
    path('rooms/<uuid:room_id>/leave/', room_views.room_leave, name='room-leave'),
    path('rooms/<uuid:room_id>/settings/', room_views.room_settings, name='room-settings'),
    
    # Room API endpoints
    path('api/rooms/<uuid:room_id>/messages/', room_api.RoomMessagesAPI.as_view(), name='api-room-messages'),
    path('api/rooms/<uuid:room_id>/members/', room_api.RoomMembersAPI.as_view(), name='api-room-members'),
    path('api/rooms/<uuid:room_id>/typing/', room_api.RoomTypingAPI.as_view(), name='api-room-typing'),
    path('api/rooms/<uuid:room_id>/files/', room_api.RoomFilesAPI.as_view(), name='api-room-files'),
    path('api/rooms/<uuid:room_id>/bot/toggle/', room_api.RoomBotToggleAPI.as_view(), name='api-room-bot-toggle'),
    path('api/rooms/<uuid:room_id>/files/<uuid:file_id>/chat/', room_api.RoomFileChatAPI.as_view(), name='api-file-chat'),
    path('api/rooms/<uuid:room_id>/messages/<uuid:message_id>/pin/', room_api.RoomPinMessageAPI.as_view(), name='api-pin-message'),
]

