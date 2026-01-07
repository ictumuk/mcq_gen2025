from django.db import models
from django.contrib.auth.models import AbstractUser
from django.core.validators import MinValueValidator
import uuid

# Shared difficulty choices for consistency across models
DIFFICULTY_LEVELS = [
    ('easy', 'Easy'),
    ('medium', 'Medium'),
    ('hard', 'Hard'),
]


# ============== USER MODEL ==============

class User(AbstractUser):
    """
    Extended User model with credits system.
    Inherits: username, email, password, first_name, last_name, etc.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    credits = models.IntegerField(
        default=100, 
        validators=[MinValueValidator(0)],
        help_text="Number of question generation credits remaining"
    )
    
    class Meta:
        db_table = 'users'
        verbose_name = 'User'
        verbose_name_plural = 'Users'
    
    def __str__(self):
        return self.email or self.username
    
    def use_credits(self, amount: int = 1) -> bool:
        """Deduct credits if available, return True if successful"""
        if self.credits >= amount:
            self.credits -= amount
            self.save(update_fields=['credits'])
            return True
        return False


# ============== SOURCE FILE MODEL ==============

class SourceFile(models.Model):
    """
    Store uploaded files (PDF/Word/Text) for question generation.
    """
    FILE_TYPES = [
        ('pdf', 'PDF'),
        ('docx', 'Word Document'),
        ('txt', 'Plain Text'),
        ('image', 'Image'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='source_files'
    )
    file_name = models.CharField(max_length=255)
    file_type = models.CharField(max_length=10, choices=FILE_TYPES)
    file = models.FileField(upload_to='source_files/%Y/%m/')
    extracted_text = models.TextField(
        blank=True, 
        help_text="OCR/extracted text content for reuse"
    )
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'source_files'
        ordering = ['-uploaded_at']
    
    def __str__(self):
        return f"{self.file_name} ({self.user})"


# ============== EXTRACTED MEDIA MODEL ==============

class ExtractedMedia(models.Model):
    """
    Store images/charts extracted from source files (for multimodal support).
    """
    MEDIA_TYPES = [
        ('image', 'Image'),
        ('chart', 'Chart/Graph'),
        ('table', 'Table Image'),
        ('diagram', 'Diagram'),
    ]
    
    id = models.CharField(max_length=50, primary_key=True)  
    source_file = models.ForeignKey(
        SourceFile, 
        on_delete=models.CASCADE, 
        related_name='extracted_media'
    )
    media_file = models.ImageField(upload_to='extracted_media/%Y/%m/')
    media_type = models.CharField(max_length=20, choices=MEDIA_TYPES)
    context_snippet = models.TextField(
        blank=True, 
        help_text="Surrounding text for context/search"
    )
    page_number = models.IntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'extracted_media'
        verbose_name_plural = 'Extracted Media'
    
    def __str__(self):
        return f"{self.id} - {self.media_type}"


# ============== SUBJECT MODEL (History) ==============

class Subject(models.Model):
    """
    A batch/session of generated questions (History).
    Maps to one generation request from user.
    """
    SOURCE_TYPES = [
        ('text', 'Direct Text Input'),
        ('file', 'Uploaded File'),
        ('url', 'URL'),
    ]
    
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('generating_contexts', 'Generating Contexts'),
        ('reviewing_contexts', 'Reviewing Contexts'),
        ('generating_mcqs', 'Generating MCQs'),
        ('reviewing_mcqs', 'Reviewing MCQs'),
        ('completed', 'Completed'),
        ('failed', 'Failed'),
    ]
    
    BLOOM_LEVELS = [
        ('Remember', 'Remember'),
        ('Understand', 'Understand'),
        ('Apply', 'Apply'),
        ('Analyze', 'Analyze'),
        ('Evaluate', 'Evaluate'),
        ('Create', 'Create'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='subjects'
    )
    title = models.CharField(max_length=255, blank=True)
    
    # Source configuration
    source_type = models.CharField(max_length=10, choices=SOURCE_TYPES, default='text')
    source_file = models.ForeignKey(
        SourceFile, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='subjects'
    )
    source_text = models.TextField(
        blank=True, 
        help_text="Direct text input or extracted text"
    )
    source_url = models.URLField(blank=True)
    
    # Generation configuration (matching GraphState in main.py)
    subject = models.CharField(max_length=100, blank=True)
    topic = models.CharField(max_length=200, blank=True)
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_LEVELS,
        default='medium',
        help_text="Normalized difficulty (easy/medium/hard)"
    )
    bloom_level = models.CharField(max_length=20, choices=BLOOM_LEVELS, default='Understand')
    number_questions = models.IntegerField(
        default=5, 
        validators=[MinValueValidator(1)],
        help_text="Target number of questions to generate"
    )
    key_points = models.TextField(blank=True, help_text="Key points to focus on")
    exercises = models.TextField(blank=True, help_text="Related exercises")
    
    # Additional config stored as JSON
    config = models.JSONField(
        default=dict, 
        blank=True,
        help_text="Additional generation config: model, max_iterations, etc."
    )
    
    # Status tracking
    status = models.CharField(max_length=30, choices=STATUS_CHOICES, default='pending')
    error_message = models.TextField(blank=True)
    
    # LangGraph state tracking
    thread_id = models.CharField(
        max_length=100, 
        blank=True,
        help_text="LangGraph thread ID for resuming"
    )
    current_stage = models.CharField(max_length=50, blank=True)
    iteration_count = models.IntegerField(default=0)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    completed_at = models.DateTimeField(null=True, blank=True)
    
    # Credits used
    credits_used = models.IntegerField(default=0)
    
    class Meta:
        db_table = 'subjects'
        ordering = ['-created_at']
        verbose_name = 'Subject'
        verbose_name_plural = 'Subjects'
    
    def __str__(self):
        return f"{self.title or 'Untitled'} - {self.user} ({self.status})"
    
    @property
    def question_count(self):
        return self.questions.count()


# ============== CONTEXT MODEL ==============

class Context(models.Model):
    """
    Store generated contexts (intermediate step in MCQ generation).
    Maps to ContextItem in main.py GraphState.
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE, 
        related_name='contexts'
    )
    
    # Content
    content = models.TextField(help_text="Generated context content")
    original_content = models.TextField(
        blank=True, 
        help_text="Original content before refinement"
    )
    
    # Review & refinement tracking (matching ContextItem)
    review_feedback = models.TextField(blank=True)
    suggestions = models.JSONField(default=list, blank=True)
    is_approved = models.BooleanField(default=False)
    iteration_count = models.IntegerField(default=0)
    
    # Order
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'contexts'
        ordering = ['subject', 'order']
    
    def __str__(self):
        return f"Context {self.order} - {self.subject}"


# ============== QUESTION MODEL ==============

class Question(models.Model):
    """
    Individual question with full MCQ structure.
    Maps to MCQItem/Question schema in gen.py.
    """
    QUESTION_TYPES = [
        ('mcq', 'Multiple Choice'),
        ('true_false', 'True/False'),
        ('essay', 'Essay'),
        ('fill_blank', 'Fill in the Blank'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE, 
        related_name='questions'
    )
    context = models.ForeignKey(
        Context, 
        on_delete=models.SET_NULL, 
        null=True,
        blank=True,
        related_name='questions',
        help_text="Source context this question was generated from"
    )
    
    # Question content (matching Question schema in gen.py)
    question_type = models.CharField(max_length=20, choices=QUESTION_TYPES, default='mcq')
    stem = models.TextField(help_text="Question stem/content")
    difficulty = models.CharField(
        max_length=10,
        choices=DIFFICULTY_LEVELS,
        default='medium',
        help_text="Normalized difficulty (easy/medium/hard)"
    )
    
    # Options stored as JSON array (matching gen.py Options schema)
    # Format: [{"id": "A", "text": "...", "is_correct": false}, ...]
    options = models.JSONField(
        default=list,
        help_text='[{"id": "A", "text": "...", "is_correct": false}, ...]'
    )
    correct_answer = models.CharField(max_length=10, help_text="Correct option ID (A, B, C, D)")
    
    # Reasoning/Explanation (matching Reason schema in gen.py)
    explanation = models.TextField(blank=True, help_text="Answer explanation")
    reasoning = models.JSONField(
        default=dict,
        blank=True,
        help_text="Full reasoning: bloom_level_analysis, tactic_analysis, etc."
    )
    
    # Media reference for multimodal questions
    media = models.ForeignKey(
        ExtractedMedia, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='questions'
    )
    
    # Review & refinement tracking (matching MCQItem)
    review_feedback = models.TextField(blank=True)
    suggestions = models.JSONField(default=list, blank=True)
    is_approved = models.BooleanField(default=False)
    
    # User editing tracking
    user_edited = models.BooleanField(
        default=False, 
        help_text="True if user manually edited this question"
    )
    original_data = models.JSONField(
        default=dict,
        blank=True,
        help_text="Original AI-generated data before user edits"
    )
    
    # Order
    order = models.IntegerField(default=0)
    
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'questions'
        ordering = ['subject', 'order']
    
    def __str__(self):
        return f"Q{self.order}: {self.stem[:50]}..."
    
    def to_mcq_dict(self):
        """Convert to dict format matching gen.py MCQ schema"""
        return {
            "question": {
                "stem": self.stem,
                "options": {"options": self.options},
                "correct_answer": self.correct_answer,
                "reasoning": self.reasoning
            }
        }
    
    @classmethod
    def from_mcq_dict(cls, mcq_dict: dict, subject, context=None, order=0, difficulty="medium"):
        """Create Question from gen.py MCQ output dict"""
        q = mcq_dict.get('question', mcq_dict)
        options = q.get('options', {})
        if isinstance(options, dict):
            options = options.get('options', [])
        
        return cls(
            subject=subject,
            context=context,
            stem=q.get('stem', ''),
            options=options,
            correct_answer=q.get('correct_answer', ''),
            difficulty=difficulty,
            reasoning=q.get('reasoning', {}),
            explanation=q.get('reasoning', {}).get('answer_justification', ''),
            order=order
        )


# ============== GENERATION LOG MODEL (Optional - for debugging) ==============

class GenerationLog(models.Model):
    """
    Log each step of the generation process for debugging/analytics.
    """
    LOG_TYPES = [
        ('context_gen', 'Context Generation'),
        ('context_review', 'Context Review'),
        ('context_refine', 'Context Refinement'),
        ('mcq_gen', 'MCQ Generation'),
        ('mcq_review', 'MCQ Review'),
        ('mcq_refine', 'MCQ Refinement'),
        ('error', 'Error'),
        ('human_feedback', 'Human Feedback'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    subject = models.ForeignKey(
        Subject, 
        on_delete=models.CASCADE, 
        related_name='logs'
    )
    
    log_type = models.CharField(max_length=30, choices=LOG_TYPES)
    message = models.TextField()
    data = models.JSONField(default=dict, blank=True)
    
    # Performance tracking
    duration_ms = models.IntegerField(null=True, blank=True)
    tokens_used = models.IntegerField(null=True, blank=True)
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'generation_logs'
        ordering = ['subject', 'created_at']
    
    def __str__(self):
        return f"[{self.log_type}] {self.message[:50]}"


# =============================================================================
# Chat Room Models (Internal Chat System)
# =============================================================================

class ChatRoom(models.Model):
    """
    Chat room model for group discussions
    """
    ROOM_TYPE_CHOICES = [
        ('community', 'Cộng đồng'),
        ('work', 'Công việc'),
        ('ai_deep', 'Chuyên sâu AI'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    name = models.CharField(max_length=100, verbose_name='Tên phòng')
    description = models.TextField(blank=True, null=True, verbose_name='Mô tả')
    room_type = models.CharField(
        max_length=20, 
        choices=ROOM_TYPE_CHOICES, 
        default='community',
        verbose_name='Loại phòng'
    )
    
    # Security
    has_password = models.BooleanField(default=False, verbose_name='Có mật khẩu')
    password_hash = models.CharField(max_length=255, blank=True, null=True)
    
    # Features
    bot_enabled = models.BooleanField(default=True, verbose_name='Bật chatbot')
    
    # Metadata
    created_by = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='created_rooms',
        verbose_name='Người tạo'
    )
    created_at = models.DateTimeField(auto_now_add=True, verbose_name='Ngày tạo')
    updated_at = models.DateTimeField(auto_now=True)
    is_active = models.BooleanField(default=True)
    
    class Meta:
        db_table = 'chat_rooms'
        ordering = ['-created_at']
        verbose_name = 'Phòng Chat'
        verbose_name_plural = 'Phòng Chat'
    
    def __str__(self):
        return self.name
    
    @property
    def online_count(self):
        """Get number of online members"""
        return self.members.filter(status='online').count()
    
    @property
    def member_count(self):
        """Get total member count"""
        return self.members.count()


class ChatRoomMember(models.Model):
    """
    Room membership with status and role
    """
    STATUS_CHOICES = [
        ('online', 'Online'),
        ('away', 'Away'),
        ('busy', 'Busy'),
        ('offline', 'Offline'),
    ]
    
    ROLE_CHOICES = [
        ('host', 'Host'),
        ('moderator', 'Moderator'),
        ('member', 'Member'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(
        ChatRoom, 
        on_delete=models.CASCADE, 
        related_name='members'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE, 
        related_name='room_memberships'
    )
    
    status = models.CharField(
        max_length=10, 
        choices=STATUS_CHOICES, 
        default='offline'
    )
    role = models.CharField(
        max_length=10, 
        choices=ROLE_CHOICES, 
        default='member'
    )
    
    # Tracking
    joined_at = models.DateTimeField(auto_now_add=True)
    last_seen = models.DateTimeField(auto_now=True)
    is_typing = models.BooleanField(default=False)
    typing_since = models.DateTimeField(null=True, blank=True)
    
    class Meta:
        db_table = 'chat_room_members'
        unique_together = ['room', 'user']
        verbose_name = 'Thành viên phòng'
        verbose_name_plural = 'Thành viên phòng'
    
    def __str__(self):
        return f"{self.user.username} in {self.room.name}"


class RoomMessage(models.Model):
    """
    Chat messages in a room
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(
        ChatRoom, 
        on_delete=models.CASCADE, 
        related_name='messages'
    )
    sender = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True, 
        blank=True,
        related_name='room_messages'
    )
    
    content = models.TextField(verbose_name='Nội dung')
    
    # Message type
    is_bot_message = models.BooleanField(default=False, verbose_name='Tin nhắn từ Bot')
    is_system_message = models.BooleanField(default=False, verbose_name='Tin nhắn hệ thống')
    
    # Threading (for replies)
    parent_message = models.ForeignKey(
        'self', 
        on_delete=models.CASCADE, 
        null=True, 
        blank=True,
        related_name='thread_replies'
    )
    
    # Features
    is_pinned = models.BooleanField(default=False, verbose_name='Đã ghim')
    
    # Mentions (stored as JSON array of user IDs)
    mentions = models.JSONField(default=list, blank=True)
    
    # Timestamps
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    
    class Meta:
        db_table = 'room_messages'
        ordering = ['created_at']
        verbose_name = 'Tin nhắn phòng'
        verbose_name_plural = 'Tin nhắn phòng'
    
    def __str__(self):
        sender_name = self.sender.username if self.sender else 'Bot'
        return f"{sender_name}: {self.content[:50]}..."
    
    @property
    def thread_count(self):
        """Get number of replies in thread"""
        return self.thread_replies.count()


class RoomFile(models.Model):
    """
    Files shared in a room
    """
    FILE_TYPE_CHOICES = [
        ('pdf', 'PDF'),
        ('docx', 'Word Document'),
        ('xlsx', 'Excel Spreadsheet'),
        ('image', 'Image'),
        ('other', 'Other'),
    ]
    
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    room = models.ForeignKey(
        ChatRoom, 
        on_delete=models.CASCADE, 
        related_name='files'
    )
    uploaded_by = models.ForeignKey(
        User, 
        on_delete=models.SET_NULL, 
        null=True,
        related_name='uploaded_room_files'
    )
    
    name = models.CharField(max_length=255, verbose_name='Tên file')
    file = models.FileField(upload_to='room_files/%Y/%m/', verbose_name='File')
    file_type = models.CharField(
        max_length=10, 
        choices=FILE_TYPE_CHOICES, 
        default='other'
    )
    file_size = models.BigIntegerField(default=0, verbose_name='Kích thước (bytes)')
    
    # RAG support
    extracted_text = models.TextField(
        blank=True, 
        null=True, 
        verbose_name='Nội dung trích xuất'
    )
    is_processed = models.BooleanField(default=False, verbose_name='Đã xử lý')
    
    # Timestamps
    uploaded_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'room_files'
        ordering = ['-uploaded_at']
        verbose_name = 'File phòng'
        verbose_name_plural = 'Files phòng'
    
    def __str__(self):
        return self.name


class FileChatMessage(models.Model):
    """
    Chat messages for file-specific RAG conversations
    """
    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    file = models.ForeignKey(
        RoomFile, 
        on_delete=models.CASCADE, 
        related_name='chat_messages'
    )
    user = models.ForeignKey(
        User, 
        on_delete=models.CASCADE,
        related_name='file_chat_messages'
    )
    
    question = models.TextField(verbose_name='Câu hỏi')
    answer = models.TextField(verbose_name='Câu trả lời')
    
    created_at = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        db_table = 'file_chat_messages'
        ordering = ['created_at']
        verbose_name = 'Hội thoại file'
        verbose_name_plural = 'Hội thoại file'
    
    def __str__(self):
        return f"Q: {self.question[:50]}..."

