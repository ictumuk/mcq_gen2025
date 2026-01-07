
import os
import shutil
from django.conf import settings
from genmcq.models import (
    SourceFile, ExtractedMedia, Subject, Context, Question, GenerationLog,
    ChatRoom, ChatRoomMember, RoomMessage, RoomFile, FileChatMessage
)

def reset_all_without_auth():
    print("Starting reset (keeping Users)...")

    # 1. Delete DB Records
    # Deleting parents usually cascades, but explicit deletion is clearer for logs
    
    print(f"Deleting {GenerationLog.objects.count()} GenerationLogs...")
    GenerationLog.objects.all().delete()

    print(f"Deleting {Question.objects.count()} Questions...")
    Question.objects.all().delete()

    print(f"Deleting {Context.objects.count()} Contexts...")
    Context.objects.all().delete()

    print(f"Deleting {Subject.objects.count()} Subjects...")
    Subject.objects.all().delete()

    print(f"Deleting {ExtractedMedia.objects.count()} ExtractedMedia...")
    ExtractedMedia.objects.all().delete()

    print(f"Deleting {SourceFile.objects.count()} SourceFiles...")
    SourceFile.objects.all().delete()

    print(f"Deleting {FileChatMessage.objects.count()} FileChatMessages...")
    FileChatMessage.objects.all().delete()

    print(f"Deleting {RoomMessage.objects.count()} RoomMessages...")
    RoomMessage.objects.all().delete()

    print(f"Deleting {RoomFile.objects.count()} RoomFiles...")
    RoomFile.objects.all().delete()

    print(f"Deleting {ChatRoomMember.objects.count()} ChatRoomMembers...")
    ChatRoomMember.objects.all().delete()

    print(f"Deleting {ChatRoom.objects.count()} ChatRooms...")
    ChatRoom.objects.all().delete()

    # 2. Cleanup Media Files
    media_root = settings.MEDIA_ROOT
    dirs_to_clean = ['source_files', 'extracted_media', 'room_files']
    
    for d in dirs_to_clean:
        dir_path = os.path.join(media_root, d)
        if os.path.exists(dir_path):
            print(f"Removing media directory: {dir_path}")
            shutil.rmtree(dir_path)
            # Recreate empty directory to avoid errors if something expects it
            os.makedirs(dir_path, exist_ok=True)
        else:
            print(f"Directory not found (skipping): {dir_path}")

    print("Reset complete. Users preserved.")

if __name__ == '__main__':
    reset_all_without_auth()
