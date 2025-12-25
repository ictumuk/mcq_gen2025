from django.urls import path
from . import views

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
    
]
