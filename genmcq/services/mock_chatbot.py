"""
Mock Chatbot Service for Chat Room
Provides keyword-based responses for testing
CR-BE-001, CR-BE-002, CR-BE-003
"""


class MockChatBot:
    """
    Mock chatbot with keyword-based responses
    """
    
    # Predefined responses
    RESPONSES = {
        '/help': '📚 **Các lệnh có sẵn:**\n• `/summary` - Tóm tắt cuộc trò chuyện\n• `/status` - Trạng thái phòng\n• `/members` - Danh sách thành viên\n• `@bot + câu hỏi` - Hỏi bot\n• `/clear` - Xóa lịch sử chat của bạn',
        
        '/summary': '📝 **Tóm tắt:**\n• Có nhiều tin nhắn mới trong phòng\n• Chủ đề chính: Thảo luận nhóm\n• Hoạt động: Đang sôi nổi\n• Số file chia sẻ: {file_count}',
        
        '/status': '📊 **Trạng thái phòng:**\n• Thành viên online: {online_count}\n• Tổng thành viên: {member_count}\n• Bot: {bot_status}\n• Phòng tạo lúc: {created_at}',
        
        '/members': '👥 **Thành viên:**\n{member_list}',
        
        'chào bot': '👋 Chào bạn! Tôi là trợ lý ảo của phòng. Gõ `/help` để xem các lệnh hữu ích.',
        
        'xin chào': '👋 Xin chào! Tôi có thể giúp gì cho bạn? Gõ `/help` để xem các lệnh.',
    }
    
    WELCOME_MESSAGE = '🤖 Bot đã tham gia phòng! Gõ `/help` để xem các lệnh.'
    NEW_MEMBER_MESSAGE = '👋 Chào mừng **{username}** đến với phòng!'
    GOODBYE_MESSAGE = '👋 **{username}** đã rời phòng.'
    
    def __init__(self, room=None):
        self.room = room
    
    def get_response(self, message_content, context=None):
        """
        Get bot response based on message content
        
        Args:
            message_content: The user's message
            context: Optional dict with room context (member_count, file_count, etc.)
            
        Returns:
            str or None: Bot response, or None if no response needed
        """
        content_lower = message_content.lower().strip()
        context = context or {}
        
        # Check for exact command matches
        for keyword, response in self.RESPONSES.items():
            if content_lower == keyword or content_lower.startswith(keyword + ' '):
                return self._format_response(response, context)
        
        # Check for keyword matches
        if 'chào' in content_lower and 'bot' in content_lower:
            return self._format_response(self.RESPONSES.get('chào bot'), context)
        
        # Check for @bot mention
        if '@bot' in content_lower:
            question = content_lower.replace('@bot', '').strip()
            return self._generate_ai_response(question, context)
        
        return None
    
    def _format_response(self, template, context):
        """Format response template with context variables"""
        if not template:
            return None
            
        return template.format(
            online_count=context.get('online_count', 0),
            member_count=context.get('member_count', 0),
            file_count=context.get('file_count', 0),
            bot_status='Đang hoạt động' if context.get('bot_enabled', True) else 'Tắt',
            created_at=context.get('created_at', 'N/A'),
            member_list=context.get('member_list', 'Chưa có thành viên'),
        )
    
    def _generate_ai_response(self, question, context):
        """
        Generate AI response (mock version)
        In production, this would call actual AI service
        """
        question_lower = question.lower()
        
        if not question:
            return '🤖 Bạn muốn hỏi gì? Hãy gõ @bot kèm câu hỏi của bạn.'
        
        # Mock AI responses based on keywords
        if 'giúp' in question_lower or 'help' in question_lower:
            return '🤖 Tôi có thể giúp bạn:\n• Trả lời câu hỏi về nội dung file\n• Tóm tắt cuộc trò chuyện\n• Cung cấp thông tin phòng\n\nHãy hỏi cụ thể hơn nhé!'
        
        if 'bạn là ai' in question_lower or 'who are you' in question_lower:
            return '🤖 Tôi là trợ lý AI của phòng chat. Tôi có thể giúp trả lời câu hỏi và hỗ trợ các thành viên trong phòng.'
        
        if 'cảm ơn' in question_lower or 'thank' in question_lower:
            return '🤖 Không có gì! Rất vui được giúp đỡ bạn. 😊'
        
        # Default response
        return f'🤖 Đây là phản hồi mẫu cho câu hỏi: "{question}"\n\nTrong phiên bản thực tế, tôi sẽ sử dụng AI để đưa ra câu trả lời chi tiết hơn.'
    
    def get_welcome_message(self):
        """Get welcome message when bot joins room"""
        return self.WELCOME_MESSAGE
    
    def get_new_member_message(self, username):
        """Get message when new member joins"""
        return self.NEW_MEMBER_MESSAGE.format(username=username)
    
    def get_goodbye_message(self, username):
        """Get message when member leaves"""
        return self.GOODBYE_MESSAGE.format(username=username)


# Singleton instance for easy import
mock_bot = MockChatBot()


def get_bot_response(message_content, room=None):
    """
    Convenience function to get bot response
    
    Args:
        message_content: User's message
        room: Optional ChatRoom instance for context
        
    Returns:
        str or None: Bot response
    """
    context = {}
    if room:
        context = {
            'online_count': room.online_count,
            'member_count': room.member_count,
            'file_count': room.files.count(),
            'bot_enabled': room.bot_enabled,
            'created_at': room.created_at.strftime('%d/%m/%Y %H:%M'),
            'member_list': '\n'.join([
                f"• {m.user.username} ({m.role})" 
                for m in room.members.all()[:10]
            ]) or 'Chưa có thành viên',
        }
    
    bot = MockChatBot(room)
    return bot.get_response(message_content, context)
