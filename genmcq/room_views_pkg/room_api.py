"""
Room API views for Chat Room functionality
RESTful APIs for messages, members, files, bot, typing
"""
from django.http import JsonResponse
from django.views import View
from django.views.decorators.csrf import csrf_exempt
from django.utils.decorators import method_decorator
from django.contrib.auth.decorators import login_required
from django.shortcuts import get_object_or_404
from django.utils import timezone
import json

from ..models import ChatRoom, ChatRoomMember, RoomMessage, RoomFile


class LoginRequiredMixin:
    """Mixin to require login for API views"""
    @method_decorator(login_required)
    def dispatch(self, request, *args, **kwargs):
        return super().dispatch(request, *args, **kwargs)


class RoomMessagesAPI(LoginRequiredMixin, View):
    """
    GET: List messages (with ?after=id for polling)
    POST: Send new message
    """
    
    def get(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        
        # Check membership for reading messages
        if not room.members.filter(user=request.user).exists():
            return JsonResponse({'error': 'Not a member'}, status=403)
        
        after_id = request.GET.get('after')
        
        messages = room.messages.select_related('sender')
        
        if after_id:
            try:
                messages = messages.filter(id__gt=after_id)
            except (ValueError, TypeError):
                pass
        else:
            messages = messages.order_by('-created_at')[:50]
            messages = reversed(list(messages))
        
        data = {
            'messages': [
                {
                    'id': str(msg.id),
                    'content': msg.content,
                    'sender': msg.sender.username if msg.sender else 'System',
                    'sender_id': msg.sender.id if msg.sender else None,
                    'is_mine': msg.sender == request.user if msg.sender else False,
                    'is_bot': msg.is_bot_message,
                    'is_pinned': msg.is_pinned,
                    'thread_count': msg.thread_count,
                    'time': msg.created_at.strftime('%H:%M'),
                    'created_at': msg.created_at.isoformat(),
                }
                for msg in messages
            ]
        }
        return JsonResponse(data)
    
    def post(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        
        # Check membership
        membership = ChatRoomMember.objects.filter(
            room=room, user=request.user
        ).first()
        if not membership:
            return JsonResponse({'error': 'Not a member'}, status=403)
        
        try:
            if request.content_type == 'application/json':
                data = json.loads(request.body)
                content = data.get('content', '')
            else:
                content = request.POST.get('content', '')
        except json.JSONDecodeError:
            content = request.POST.get('content', '')
        
        if not content.strip():
            return JsonResponse({'error': 'Content is required'}, status=400)
        
        # Parse mentions
        mentions = []
        import re
        mention_pattern = r'@(\w+)'
        for match in re.finditer(mention_pattern, content):
            username = match.group(1)
            from ..models import User
            user = User.objects.filter(username__iexact=username).first()
            if user:
                mentions.append(user.id)
        
        # Create message
        msg = RoomMessage.objects.create(
            room=room,
            sender=request.user,
            content=content,
            mentions=mentions
        )
        
        # Check for bot commands if bot is enabled
        if room.bot_enabled:
            bot_response = self._process_bot_command(content)
            if bot_response:
                RoomMessage.objects.create(
                    room=room,
                    sender=None,
                    content=bot_response,
                    is_bot_message=True
                )
        
        return JsonResponse({
            'success': True,
            'message': {
                'id': str(msg.id),
                'content': msg.content,
                'time': msg.created_at.strftime('%H:%M'),
            }
        })
    
    def _process_bot_command(self, content):
        """Process bot commands and return response"""
        content_lower = content.lower().strip()
        
        # Bot responses
        responses = {
            '/help': '📚 Các lệnh có sẵn:\n• /summary - Tóm tắt chat\n• /status - Trạng thái phòng\n• @bot + câu hỏi - Hỏi bot',
            '/summary': '📝 Tóm tắt:\n• Nhiều tin nhắn mới trong phòng\n• Chủ đề chính: Thảo luận nhóm\n• Hoạt động: Đang sôi nổi',
            '/status': '📊 Trạng thái phòng:\n• Thành viên đang online\n• Bot: Đang hoạt động\n• Files: Có thể chia sẻ',
            'chào bot': '👋 Chào bạn! Tôi là trợ lý ảo của phòng. Gõ /help để xem các lệnh.',
        }
        
        for keyword, response in responses.items():
            if keyword in content_lower:
                return response
        
        # Check for @bot mention
        if '@bot' in content_lower:
            return '🤖 Tôi đã nhận câu hỏi của bạn. Đây là phản hồi mẫu. Trong phiên bản thực tế, tôi sẽ sử dụng AI để trả lời chi tiết hơn.'
        
        return None


class RoomMembersAPI(LoginRequiredMixin, View):
    """
    GET: List members with status
    """
    
    def get(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        
        members = room.members.select_related('user')
        
        # Get typing users (active in last 5 seconds)
        typing_threshold = timezone.now() - timezone.timedelta(seconds=5)
        typing_users = [
            m.user.username 
            for m in members 
            if m.is_typing and m.typing_since and m.typing_since > typing_threshold
        ]
        
        data = {
            'members': [
                {
                    'id': m.user.id,
                    'name': m.user.get_full_name() or m.user.username,
                    'username': m.user.username,
                    'status': m.status,
                    'role': m.role,
                    'is_typing': m.is_typing,
                }
                for m in members
            ],
            'typing_users': typing_users,
        }
        return JsonResponse(data)


class RoomTypingAPI(LoginRequiredMixin, View):
    """
    POST: Send typing indicator
    """
    
    def post(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        
        membership = ChatRoomMember.objects.filter(
            room=room, user=request.user
        ).first()
        
        if membership:
            membership.is_typing = True
            membership.typing_since = timezone.now()
            membership.save()
        
        return JsonResponse({'success': True})


class RoomFilesAPI(LoginRequiredMixin, View):
    """
    GET: List files in room
    POST: Upload file
    """
    
    def get(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        
        files = room.files.select_related('uploaded_by')
        
        data = {
            'files': [
                {
                    'id': str(f.id),
                    'name': f.name,
                    'type': f.file_type,
                    'size': self._format_size(f.file_size),
                    'uploaded_by': f.uploaded_by.username if f.uploaded_by else 'Unknown',
                    'uploaded_at': f.uploaded_at.isoformat(),
                }
                for f in files
            ]
        }
        return JsonResponse(data)
    
    def post(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        
        # Check membership
        membership = ChatRoomMember.objects.filter(
            room=room, user=request.user
        ).first()
        if not membership:
            return JsonResponse({'error': 'Not a member'}, status=403)
        
        file = request.FILES.get('file')
        if not file:
            return JsonResponse({'error': 'No file provided'}, status=400)
        
        # Create file record
        room_file = RoomFile.objects.create(
            room=room,
            uploaded_by=request.user,
            name=file.name,
            file=file,
            file_size=file.size
        )
        
        # Add system message
        RoomMessage.objects.create(
            room=room,
            sender=request.user,
            content=f'📎 Đã chia sẻ file: {file.name}',
            is_system_message=True
        )
        
        return JsonResponse({
            'success': True,
            'file': {
                'id': str(room_file.id),
                'name': room_file.name,
                'type': room_file.file_type,
            }
        })
    
    def _format_size(self, size_bytes):
        """Format file size to human readable"""
        for unit in ['B', 'KB', 'MB', 'GB']:
            if size_bytes < 1024:
                return f"{size_bytes:.1f} {unit}"
            size_bytes /= 1024
        return f"{size_bytes:.1f} TB"


class RoomBotToggleAPI(LoginRequiredMixin, View):
    """
    POST: Toggle bot on/off
    """
    
    def post(self, request, room_id):
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        
        # Check if moderator or host
        membership = ChatRoomMember.objects.filter(
            room=room, 
            user=request.user,
            role__in=['host', 'moderator']
        ).first()
        
        if not membership:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        try:
            data = json.loads(request.body)
            enabled = data.get('enabled', not room.bot_enabled)
        except json.JSONDecodeError:
            enabled = not room.bot_enabled
        
        room.bot_enabled = enabled
        room.save()
        
        # Add system message
        RoomMessage.objects.create(
            room=room,
            sender=None,
            content=f'🤖 Bot đã được {"bật" if enabled else "tắt"}',
            is_system_message=True,
            is_bot_message=True
        )
        
        return JsonResponse({
            'success': True,
            'bot_enabled': room.bot_enabled
        })


class RoomFileChatAPI(LoginRequiredMixin, View):
    """
    POST: Chat with file (RAG mode)
    """
    
    def post(self, request, room_id, file_id):
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        room_file = get_object_or_404(RoomFile, id=file_id, room=room)
        
        # Check membership
        membership = ChatRoomMember.objects.filter(
            room=room, user=request.user
        ).first()
        if not membership:
            return JsonResponse({'error': 'Not a member'}, status=403)
        
        try:
            data = json.loads(request.body)
            question = data.get('question', '')
        except json.JSONDecodeError:
            question = request.POST.get('question', '')
        
        if not question.strip():
            return JsonResponse({'error': 'Question is required'}, status=400)
        
        # Mock RAG response (in real app, this would use AI)
        answer = self._generate_mock_answer(question, room_file)
        
        # Save to file chat history
        from ..models import FileChatMessage
        FileChatMessage.objects.create(
            file=room_file,
            user=request.user,
            question=question,
            answer=answer
        )
        
        return JsonResponse({
            'success': True,
            'answer': answer
        })
    
    def _generate_mock_answer(self, question, room_file):
        """Generate mock answer based on question"""
        question_lower = question.lower()
        
        if 'tóm tắt' in question_lower or 'summary' in question_lower:
            return f'📄 Tóm tắt file "{room_file.name}":\n\nĐây là tài liệu chứa thông tin quan trọng. Các điểm chính:\n1. Nội dung điểm 1\n2. Nội dung điểm 2\n3. Nội dung điểm 3'
        elif 'ngày' in question_lower or 'date' in question_lower:
            return f'📅 File được tải lên ngày {room_file.uploaded_at.strftime("%d/%m/%Y")} bởi {room_file.uploaded_by.username if room_file.uploaded_by else "Unknown"}'
        else:
            return f'🤖 Dựa trên nội dung file "{room_file.name}", đây là phản hồi mẫu cho câu hỏi của bạn. Trong phiên bản thực tế, AI sẽ phân tích nội dung thực của file để đưa ra câu trả lời chính xác.'


class RoomPinMessageAPI(LoginRequiredMixin, View):
    """
    POST: Pin/unpin a message
    """
    
    def post(self, request, room_id, message_id):
        room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
        message = get_object_or_404(RoomMessage, id=message_id, room=room)
        
        # Check if moderator or host
        membership = ChatRoomMember.objects.filter(
            room=room, 
            user=request.user,
            role__in=['host', 'moderator']
        ).first()
        
        if not membership:
            return JsonResponse({'error': 'Permission denied'}, status=403)
        
        message.is_pinned = not message.is_pinned
        message.save()
        
        return JsonResponse({
            'success': True,
            'is_pinned': message.is_pinned
        })
