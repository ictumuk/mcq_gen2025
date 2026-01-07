"""
Room views for Chat Room pages
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import Http404
from django.contrib.auth.hashers import check_password, make_password

from ..models import ChatRoom, ChatRoomMember


@login_required
def room_list(request):
    """
    Dashboard: List of all active chat rooms
    """
    rooms = ChatRoom.objects.filter(is_active=True).prefetch_related('members')
    
    # Get user's recent rooms
    recent_memberships = ChatRoomMember.objects.filter(
        user=request.user
    ).select_related('room').order_by('-last_seen')[:5]
    
    recent_rooms = [m.room for m in recent_memberships]
    
    context = {
        'rooms': rooms,
        'recent_rooms': recent_rooms,
    }
    return render(request, 'zoom/rooms/list.html', context)


@login_required
def room_create(request):
    """
    Create a new chat room
    """
    if request.method == 'POST':
        name = request.POST.get('name', '').strip()
        description = request.POST.get('description', '').strip()
        room_type = request.POST.get('room_type', 'community')
        password = request.POST.get('password', '').strip()
        bot_enabled = request.POST.get('bot_enabled') == 'on'
        
        if not name:
            messages.error(request, 'Tên phòng không được để trống')
            return redirect('room-list')
        
        # Create room
        room = ChatRoom.objects.create(
            name=name,
            description=description,
            room_type=room_type,
            has_password=bool(password),
            password_hash=make_password(password) if password else None,
            bot_enabled=bot_enabled,
            created_by=request.user
        )
        
        # Add creator as host
        ChatRoomMember.objects.create(
            room=room,
            user=request.user,
            role='host',
            status='online'
        )
        
        messages.success(request, f'Phòng "{room.name}" đã được tạo!')
        return redirect('room-chat', room_id=str(room.id))
    
    return redirect('room-list')


@login_required
def room_join(request, room_id):
    """
    Join a chat room (with optional password)
    """
    room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
    
    # Check if already a member
    membership = ChatRoomMember.objects.filter(room=room, user=request.user).first()
    
    if membership:
        # Update status to online
        membership.status = 'online'
        membership.save()
        return redirect('room-chat', room_id=str(room.id))
    
    # Check password
    if room.has_password:
        password = request.POST.get('password') or request.GET.get('password')
        if not password or not check_password(password, room.password_hash):
            messages.error(request, 'Mật khẩu không đúng')
            return redirect('room-list')
    
    # Create membership
    ChatRoomMember.objects.create(
        room=room,
        user=request.user,
        role='member',
        status='online'
    )
    
    messages.success(request, f'Đã tham gia phòng "{room.name}"')
    return redirect('room-chat', room_id=str(room.id))


@login_required
def room_chat(request, room_id):
    """
    Chat room main page
    """
    room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
    
    # Check membership
    membership = ChatRoomMember.objects.filter(room=room, user=request.user).first()
    
    if not membership:
        messages.warning(request, 'Bạn cần tham gia phòng trước')
        return redirect('room-join', room_id=str(room.id))
    
    # Update status
    membership.status = 'online'
    membership.save()
    
    context = {
        'room': room,
        'membership': membership,
        'is_host': membership.role == 'host',
        'is_moderator': membership.role in ['host', 'moderator'],
    }
    return render(request, 'zoom/rooms/chat.html', context)


@login_required
def room_leave(request, room_id):
    """
    Leave a chat room
    """
    room = get_object_or_404(ChatRoom, id=room_id)
    
    membership = ChatRoomMember.objects.filter(room=room, user=request.user).first()
    
    if membership:
        if membership.role == 'host':
            # Transfer host or delete room
            other_member = room.members.exclude(user=request.user).first()
            if other_member:
                other_member.role = 'host'
                other_member.save()
                membership.delete()
            else:
                # No other members, delete room
                room.is_active = False
                room.save()
                membership.delete()
        else:
            membership.delete()
        
        messages.success(request, f'Đã rời khỏi phòng "{room.name}"')
    
    return redirect('room-list')


@login_required
def room_settings(request, room_id):
    """
    Room settings (host only)
    """
    room = get_object_or_404(ChatRoom, id=room_id, is_active=True)
    
    # Check if host
    membership = ChatRoomMember.objects.filter(
        room=room, 
        user=request.user, 
        role='host'
    ).first()
    
    if not membership:
        messages.error(request, 'Chỉ host mới có thể chỉnh sửa phòng')
        return redirect('room-chat', room_id=str(room.id))
    
    if request.method == 'POST':
        room.name = request.POST.get('name', room.name)
        room.description = request.POST.get('description', room.description)
        room.bot_enabled = request.POST.get('bot_enabled') == 'on'
        
        new_password = request.POST.get('new_password', '').strip()
        if new_password:
            room.has_password = True
            room.password_hash = make_password(new_password)
        elif request.POST.get('remove_password'):
            room.has_password = False
            room.password_hash = None
        
        room.save()
        messages.success(request, 'Đã cập nhật cài đặt phòng')
        return redirect('room-chat', room_id=str(room.id))
    
    context = {
        'room': room,
    }
    return render(request, 'zoom/rooms/settings.html', context)
