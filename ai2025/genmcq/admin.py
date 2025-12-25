from django.contrib import admin
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from .models import (
    User, SourceFile, ExtractedMedia, 
    Subject, Context, Question, GenerationLog
)


# ============== USER ADMIN ==============

@admin.register(User)
class UserAdmin(BaseUserAdmin):
    """Custom User admin with credits field"""
    list_display = ['username', 'email', 'credits', 'is_staff', 'date_joined']
    list_filter = ['is_staff', 'is_active', 'date_joined']
    search_fields = ['username', 'email', 'first_name', 'last_name']
    ordering = ['-date_joined']
    
    # Add credits to fieldsets
    fieldsets = BaseUserAdmin.fieldsets + (
        ('Credits', {'fields': ('credits',)}),
    )
    add_fieldsets = BaseUserAdmin.add_fieldsets + (
        ('Credits', {'fields': ('credits',)}),
    )


# ============== SOURCE FILE ADMIN ==============

@admin.register(SourceFile)
class SourceFileAdmin(admin.ModelAdmin):
    list_display = ['file_name', 'user', 'file_type', 'uploaded_at']
    list_filter = ['file_type', 'uploaded_at']
    search_fields = ['file_name', 'user__username', 'user__email']
    readonly_fields = ['uploaded_at']
    date_hierarchy = 'uploaded_at'


# ============== EXTRACTED MEDIA ADMIN ==============

@admin.register(ExtractedMedia)
class ExtractedMediaAdmin(admin.ModelAdmin):
    list_display = ['id', 'source_file', 'media_type', 'page_number', 'created_at']
    list_filter = ['media_type', 'created_at']
    search_fields = ['id', 'context_snippet']
    readonly_fields = ['created_at']


# ============== QUESTION SET ADMIN ==============

class ContextInline(admin.TabularInline):
    """Inline view of contexts in Subject"""
    model = Context
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    fields = ['order', 'content', 'is_approved', 'iteration_count']


class QuestionInline(admin.TabularInline):
    """Inline view of questions in Subject"""
    model = Question
    extra = 0
    readonly_fields = ['created_at', 'updated_at']
    fields = ['order', 'stem', 'correct_answer', 'is_approved', 'user_edited']


@admin.register(Subject)
class SubjectAdmin(admin.ModelAdmin):
    list_display = [
        'title', 'user', 'status', 'bloom_level', 
        'number_questions', 'question_count', 'credits_used', 'created_at'
    ]
    list_filter = ['status', 'bloom_level', 'source_type', 'created_at']
    search_fields = ['title', 'user__username', 'user__email', 'subject', 'topic']
    readonly_fields = ['created_at', 'updated_at', 'completed_at', 'question_count']
    date_hierarchy = 'created_at'
    
    fieldsets = (
        (None, {
            'fields': ('user', 'title', 'status')
        }),
        ('Source', {
            'fields': ('source_type', 'source_file', 'source_text', 'source_url'),
            'classes': ('collapse',)
        }),
        ('Configuration', {
            'fields': ('subject', 'topic', 'bloom_level', 'number_questions', 'key_points', 'exercises', 'config')
        }),
        ('Tracking', {
            'fields': ('thread_id', 'current_stage', 'iteration_count', 'credits_used', 'error_message'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at', 'completed_at'),
            'classes': ('collapse',)
        }),
    )
    
    inlines = [ContextInline, QuestionInline]
    
    def question_count(self, obj):
        return obj.questions.count()
    question_count.short_description = 'Questions'


# ============== CONTEXT ADMIN ==============

@admin.register(Context)
class ContextAdmin(admin.ModelAdmin):
    list_display = ['__str__', 'subject', 'is_approved', 'iteration_count', 'created_at']
    list_filter = ['is_approved', 'created_at']
    search_fields = ['content', 'subject__title']
    readonly_fields = ['created_at', 'updated_at']


# ============== QUESTION ADMIN ==============

@admin.register(Question)
class QuestionAdmin(admin.ModelAdmin):
    list_display = [
        'order', 'stem_preview', 'subject', 'question_type',
        'correct_answer', 'is_approved', 'user_edited', 'created_at'
    ]
    list_filter = ['question_type', 'is_approved', 'user_edited', 'created_at']
    search_fields = ['stem', 'subject__title', 'explanation']
    readonly_fields = ['created_at', 'updated_at']
    
    fieldsets = (
        (None, {
            'fields': ('subject', 'context', 'question_type', 'order')
        }),
        ('Content', {
            'fields': ('stem', 'options', 'correct_answer', 'explanation', 'reasoning')
        }),
        ('Media', {
            'fields': ('media',),
            'classes': ('collapse',)
        }),
        ('Review', {
            'fields': ('review_feedback', 'suggestions', 'is_approved'),
            'classes': ('collapse',)
        }),
        ('User Edits', {
            'fields': ('user_edited', 'original_data'),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )
    
    def stem_preview(self, obj):
        return obj.stem[:60] + '...' if len(obj.stem) > 60 else obj.stem
    stem_preview.short_description = 'Stem'


# ============== GENERATION LOG ADMIN ==============

@admin.register(GenerationLog)
class GenerationLogAdmin(admin.ModelAdmin):
    list_display = ['log_type', 'message_preview', 'subject', 'duration_ms', 'created_at']
    list_filter = ['log_type', 'created_at']
    search_fields = ['message', 'subject__title']
    readonly_fields = ['created_at']
    date_hierarchy = 'created_at'
    
    def message_preview(self, obj):
        return obj.message[:50] + '...' if len(obj.message) > 50 else obj.message
    message_preview.short_description = 'Message'
