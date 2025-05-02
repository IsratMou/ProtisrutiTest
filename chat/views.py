from django.shortcuts import render, get_object_or_404
from django.http import JsonResponse, HttpResponseForbidden
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from .models import ChatRoom, Message
from accounts.models import CustomUser

@login_required
def chat_home(request):
    if request.user.user_type == 'victim':
        rooms = ChatRoom.objects.filter(user=request.user)
        
        # If no chat rooms exist, let's create one with an available counselor
        if not rooms.exists():
            # Find an available counselor
            counselors = CustomUser.objects.filter(user_type='counselor')
            if counselors.exists():
                counselor = counselors.first()  # In a real app, use logic to assign best counselor
                # Create a chat room
                room = ChatRoom.objects.create(user=request.user, counselor=counselor)
                rooms = [room]
    else:
        rooms = ChatRoom.objects.filter(counselor=request.user)
    
    return render(request, 'chat/home.html', {
        'rooms': rooms,
        'is_counselor': request.user.user_type == 'counselor'
    })

@login_required
def chat_room(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in [room.user, room.counselor]:
        return HttpResponseForbidden()
    
    # Mark unread messages as read
    if request.user == room.user:
        Message.objects.filter(room=room, sender=room.counselor, read=False).update(read=True)
    else:
        Message.objects.filter(room=room, sender=room.user, read=False).update(read=True)
    
    return render(request, 'chat/room.html', {
        'room': room,
        'other_user': room.counselor if request.user == room.user else room.user
    })

# API Views
@login_required
def get_chat_rooms(request):
    if request.user.user_type == 'victim':
        rooms = ChatRoom.objects.filter(user=request.user)
    else:
        rooms = ChatRoom.objects.filter(counselor=request.user)
    
    rooms_data = []
    for room in rooms:
        other_user = room.counselor if request.user == room.user else room.user
        last_message = room.messages.last()
        
        rooms_data.append({
            'id': room.id,
            'other_user': f"{other_user.first_name} {other_user.last_name}",
            'last_message': last_message.content if last_message else "No messages yet",
            'unread_count': room.messages.filter(
                sender=other_user, 
                read=False
            ).count()
        })
    
    return JsonResponse({'rooms': rooms_data})

@login_required
def get_messages(request, room_id):
    room = get_object_or_404(ChatRoom, id=room_id)
    if request.user not in [room.user, room.counselor]:
        return HttpResponseForbidden("You don't have permission to view these messages")
    
    messages = room.messages.all().order_by('timestamp')
    
    messages_data = []
    for message in messages:
        messages_data.append({
            'sender': f"{message.sender.first_name} {message.sender.last_name}",
            'content': message.content,
            'timestamp': message.timestamp.strftime("%b %d, %Y %I:%M %p"),
            'is_me': message.sender == request.user
        })
    
    return JsonResponse({'messages': messages_data})

@login_required
@require_POST
def send_message(request):
    room_id = request.POST.get('room_id')
    content = request.POST.get('content')
    
    if not room_id or not content:
        return JsonResponse({'status': 'error', 'message': 'Missing room_id or content'}, status=400)
    
    room = get_object_or_404(ChatRoom, id=room_id)
    
    # Check if user has permission to send message in this room
    if request.user not in [room.user, room.counselor]:
        return JsonResponse({'status': 'error', 'message': 'Permission denied'}, status=403)
    
    message = Message.objects.create(
        room=room,
        sender=request.user,
        content=content
    )
    
    return JsonResponse({
        'status': 'success',
        'message': {
            'id': message.id,
            'sender': f"{message.sender.first_name} {message.sender.last_name}",
            'content': message.content,
            'timestamp': message.timestamp.strftime("%b %d, %Y %I:%M %p"),
            'is_me': True
        }
    })