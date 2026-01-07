# IMPLEMENTATION TODO: Zoom Management & AI Bot Learning System

## Overview

Danh sách các task atomic để implement hệ thống Zoom Management dựa trên SYSTEM_DESIGN_REPORT.md

---

## Phase 1: Database Layer

### 1.1 New Models

- [ ] **DB-001** | Database | Create `ZoomAccount` model với OAuth2 fields | `genmcq/models.py`
- [ ] **DB-002** | Database | Create `ZoomMeeting` model với meeting config | `genmcq/models.py`
- [ ] **DB-003** | Database | Create `ZoomParticipant` model | `genmcq/models.py`
- [ ] **DB-004** | Database | Create `ZoomRecording` model | `genmcq/models.py`
- [ ] **DB-005** | Database | Create `ZoomTranscript` model | `genmcq/models.py`
- [ ] **DB-006** | Database | Create `ZoomBot` model | `genmcq/models.py`
- [ ] **DB-007** | Database | Create `ZoomBotSession` model | `genmcq/models.py`
- [ ] **DB-008** | Database | Create `BotMessage` model | `genmcq/models.py`
- [ ] **DB-009** | Database | Create `ChatSession` model | `genmcq/models.py`
- [ ] **DB-010** | Database | Create `ChatMessage` model | `genmcq/models.py`
- [ ] **DB-011** | Database | Create `CreditTransaction` model | `genmcq/models.py`
- [ ] **DB-012** | Database | Create database migration | `python manage.py makemigrations`
- [ ] **DB-013** | Database | Apply migration | `python manage.py migrate`

### 1.2 Model Enhancements

- [ ] **DB-014** | Database | Add token encryption utility | `genmcq/utils/encryption.py`
- [ ] **DB-015** | Database | Add `encrypt_token()` và `decrypt_token()` methods cho ZoomAccount | `genmcq/models.py`

---

## Phase 2: Backend Layer

### 2.1 Configuration

- [ ] **BE-001** | Backend | Add Zoom API credentials vào `.env` | `.env`
- [ ] **BE-002** | Backend | Add Zoom settings vào Django settings | `mcq_gen2025/settings.py`
- [ ] **BE-003** | Backend | Install `requests-oauthlib` package | `requirements.txt`

### 2.2 Zoom Services

- [ ] **BE-010** | Backend | Create Zoom OAuth2 service | `genmcq/services/zoom_oauth.py`
- [ ] **BE-011** | Backend | Implement OAuth2 authorization URL generation | `zoom_oauth.py`
- [ ] **BE-012** | Backend | Implement OAuth2 callback handler | `zoom_oauth.py`
- [ ] **BE-013** | Backend | Implement token refresh logic | `zoom_oauth.py`
- [ ] **BE-014** | Backend | Create Zoom API client wrapper | `genmcq/services/zoom_api.py`
- [ ] **BE-015** | Backend | Implement create meeting API | `zoom_api.py`
- [ ] **BE-016** | Backend | Implement get meeting details API | `zoom_api.py`
- [ ] **BE-017** | Backend | Implement list meetings API | `zoom_api.py`
- [ ] **BE-018** | Backend | Implement delete meeting API | `zoom_api.py`
- [ ] **BE-019** | Backend | Implement get recordings API | `zoom_api.py`

### 2.3 Bot Services

- [ ] **BE-020** | Backend | Create Bot service module | `genmcq/services/zoom_bot.py`
- [ ] **BE-021** | Backend | Implement bot join meeting logic | `zoom_bot.py`
- [ ] **BE-022** | Backend | Implement bot leave meeting logic | `zoom_bot.py`
- [ ] **BE-023** | Backend | Create AI response handler | `genmcq/services/bot_ai.py`
- [ ] **BE-024** | Backend | Integrate Gemini AI for Q&A | `bot_ai.py`

### 2.4 Chat Services

- [ ] **BE-030** | Backend | Create Chat service | `genmcq/services/chat_service.py`
- [ ] **BE-031** | Backend | Implement document Q&A với Gemini | `chat_service.py`
- [ ] **BE-032** | Backend | Implement video Q&A với transcript | `chat_service.py`

### 2.5 Credit Services

- [ ] **BE-040** | Backend | Create Credit service | `genmcq/services/credit_service.py`
- [ ] **BE-041** | Backend | Implement credit deduction với atomic transaction | `credit_service.py`
- [ ] **BE-042** | Backend | Implement credit transaction logging | `credit_service.py`
- [ ] **BE-043** | Backend | Add credit constants/pricing | `genmcq/constants.py`

### 2.6 API Views

- [ ] **BE-050** | Backend | Create ZoomAccountViewSet | `genmcq/views/zoom_views.py`
- [ ] **BE-051** | Backend | Create ZoomMeetingViewSet | `genmcq/views/zoom_views.py`
- [ ] **BE-052** | Backend | Create ZoomBotViewSet | `genmcq/views/zoom_views.py`
- [ ] **BE-053** | Backend | Create ZoomRecordingViewSet | `genmcq/views/zoom_views.py`
- [ ] **BE-054** | Backend | Create ChatSessionViewSet | `genmcq/views/chat_views.py`
- [ ] **BE-055** | Backend | Create CreditViewSet | `genmcq/views/credit_views.py`

### 2.7 URL Routes

- [ ] **BE-060** | Backend | Add Zoom API routes | `genmcq/urls.py`
- [ ] **BE-061** | Backend | Add Chat API routes | `genmcq/urls.py`
- [ ] **BE-062** | Backend | Add Credit API routes | `genmcq/urls.py`

### 2.8 Forms

- [ ] **BE-070** | Backend | Create ZoomAccountConnectForm | `genmcq/forms.py`
- [ ] **BE-071** | Backend | Create ZoomMeetingForm | `genmcq/forms.py`
- [ ] **BE-072** | Backend | Create JoinMeetingForm | `genmcq/forms.py`

### 2.9 Admin

- [ ] **BE-080** | Backend | Register Zoom models in admin | `genmcq/admin.py`
- [ ] **BE-081** | Backend | Register Chat models in admin | `genmcq/admin.py`
- [ ] **BE-082** | Backend | Register Credit models in admin | `genmcq/admin.py`

---

## Phase 3: Frontend Layer

### 3.1 Base Template Updates

- [ ] **FE-001** | Frontend | Update navigation với Zoom, Chat, Credits links | `templates/base.html`
- [ ] **FE-002** | Frontend | Add credit balance display in header | `templates/base.html`

### 3.2 Zoom Account Pages

- [ ] **FE-010** | Frontend | Create zoom accounts list page | `templates/zoom/accounts/list.html`
- [ ] **FE-011** | Frontend | Create connect account page (OAuth) | `templates/zoom/accounts/connect.html`
- [ ] **FE-012** | Frontend | Add disconnect account confirmation modal | `templates/zoom/accounts/list.html`

### 3.3 Zoom Meeting Pages

- [ ] **FE-020** | Frontend | Create meetings list page | `templates/zoom/meetings/list.html`
- [ ] **FE-021** | Frontend | Create meeting form (create/edit) | `templates/zoom/meetings/create.html`
- [ ] **FE-022** | Frontend | Create join meeting page | `templates/zoom/meetings/join.html`
- [ ] **FE-023** | Frontend | Create meeting detail page | `templates/zoom/meetings/detail.html`
- [ ] **FE-024** | Frontend | Add participants tab in meeting detail | `templates/zoom/meetings/detail.html`
- [ ] **FE-025** | Frontend | Add recordings tab in meeting detail | `templates/zoom/meetings/detail.html`
- [ ] **FE-026** | Frontend | Add transcript viewer | `templates/zoom/meetings/detail.html`

### 3.4 Bot Pages

- [ ] **FE-030** | Frontend | Create bot settings page | `templates/zoom/bot/settings.html`
- [ ] **FE-031** | Frontend | Create bot sessions history page | `templates/zoom/bot/sessions.html`
- [ ] **FE-032** | Frontend | Create bot session detail với messages | `templates/zoom/bot/session_detail.html`

### 3.5 Chat Pages

- [ ] **FE-040** | Frontend | Create chat session page (chat UI) | `templates/chat/session.html`
- [ ] **FE-041** | Frontend | Create chat history page | `templates/chat/history.html`
- [ ] **FE-042** | Frontend | Add document selector for chat | `templates/chat/session.html`
- [ ] **FE-043** | Frontend | Add video/recording selector for chat | `templates/chat/session.html`

### 3.6 Credit Pages

- [ ] **FE-050** | Frontend | Create credit balance page | `templates/credits/balance.html`
- [ ] **FE-051** | Frontend | Create transaction history page | `templates/credits/transactions.html`
- [ ] **FE-052** | Frontend | Create purchase credits page | `templates/credits/purchase.html`

### 3.7 Components

- [ ] **FE-060** | Frontend | Create meeting card component | `templates/components/meeting_card.html`
- [ ] **FE-061** | Frontend | Create chat bubble component | `templates/components/chat_bubble.html`
- [ ] **FE-062** | Frontend | Create credit balance widget | `templates/components/credit_widget.html`
- [ ] **FE-063** | Frontend | Create participant list component | `templates/components/participant_list.html`

### 3.8 JavaScript

- [ ] **FE-070** | Frontend | Create Zoom meeting JS handler | `static/js/zoom.js`
- [ ] **FE-071** | Frontend | Create Chat WebSocket handler | `static/js/chat.js`
- [ ] **FE-072** | Frontend | Create credit animation/update | `static/js/credits.js`

### 3.9 CSS

- [ ] **FE-080** | Frontend | Add Zoom-specific styles | `static/src/zoom.css`
- [ ] **FE-081** | Frontend | Add Chat UI styles | `static/src/chat.css`

---

## Phase 4: Integration Layer

### 4.1 Zoom Webhook

- [ ] **INT-001** | Integration | Create Zoom webhook endpoint | `genmcq/views/webhooks.py`
- [ ] **INT-002** | Integration | Handle meeting.started webhook | `webhooks.py`
- [ ] **INT-003** | Integration | Handle meeting.ended webhook | `webhooks.py`
- [ ] **INT-004** | Integration | Handle recording.completed webhook | `webhooks.py`
- [ ] **INT-005** | Integration | Add webhook URL route | `genmcq/urls.py`

### 4.2 Background Tasks

- [ ] **INT-010** | Integration | Setup Celery for background tasks | `mcq_gen2025/celery.py`
- [ ] **INT-011** | Integration | Create refresh token task | `genmcq/tasks.py`
- [ ] **INT-012** | Integration | Create transcription task | `genmcq/tasks.py`
- [ ] **INT-013** | Integration | Create bot session cleanup task | `genmcq/tasks.py`

### 4.3 Real-time

- [ ] **INT-020** | Integration | Setup Django Channels | `mcq_gen2025/asgi.py`
- [ ] **INT-021** | Integration | Create Chat WebSocket consumer | `genmcq/consumers.py`
- [ ] **INT-022** | Integration | Create Bot status WebSocket consumer | `genmcq/consumers.py`

---

## Phase 5: Testing

### 5.1 Unit Tests

- [ ] **TST-001** | Testing | Test ZoomAccount model | `genmcq/tests/test_models.py`
- [ ] **TST-002** | Testing | Test ZoomMeeting model | `genmcq/tests/test_models.py`
- [ ] **TST-003** | Testing | Test CreditTransaction model | `genmcq/tests/test_models.py`
- [ ] **TST-004** | Testing | Test credit deduction logic | `genmcq/tests/test_services.py`
- [ ] **TST-005** | Testing | Test token encryption/decryption | `genmcq/tests/test_utils.py`

### 5.2 Integration Tests

- [ ] **TST-010** | Testing | Test Zoom OAuth flow (mocked) | `genmcq/tests/test_zoom_oauth.py`
- [ ] **TST-011** | Testing | Test meeting CRUD API | `genmcq/tests/test_api.py`
- [ ] **TST-012** | Testing | Test chat session API | `genmcq/tests/test_api.py`

### 5.3 Manual Testing

- [ ] **TST-020** | Testing | Manual test: Connect Zoom account flow
- [ ] **TST-021** | Testing | Manual test: Create and join meeting
- [ ] **TST-022** | Testing | Manual test: Invite bot to meeting
- [ ] **TST-023** | Testing | Manual test: Chat with document
- [ ] **TST-024** | Testing | Manual test: Credit deduction flow

---

## Implementation Order (Recommended)

```
Phase 1: Database (DB-001 → DB-015)
    ↓
Phase 2.1-2.3: Core Backend Services (BE-001 → BE-024)
    ↓
Phase 2.5: Credit System (BE-040 → BE-043)
    ↓
Phase 2.6-2.9: API & Admin (BE-050 → BE-082)
    ↓
Phase 3.1-3.2: Base Templates & Zoom Accounts UI (FE-001 → FE-012)
    ↓
Phase 3.3: Meetings UI (FE-020 → FE-026)
    ↓
Phase 3.4-3.6: Bot, Chat, Credits UI (FE-030 → FE-052)
    ↓
Phase 4: Integrations (INT-001 → INT-022)
    ↓
Phase 5: Testing (TST-001 → TST-024)
```

---

## Dependencies

### Python Packages (add to requirements.txt)

```
requests-oauthlib>=1.3.0
cryptography>=41.0.0
channels>=4.0.0
celery>=5.3.0
redis>=5.0.0
```

### Environment Variables (add to .env)

```
ZOOM_CLIENT_ID=your_zoom_client_id
ZOOM_CLIENT_SECRET=your_zoom_client_secret
ZOOM_REDIRECT_URI=http://localhost:8000/api/zoom/accounts/callback/
ZOOM_BOT_ACCOUNT_EMAIL=bot@yourdomain.com
ENCRYPTION_KEY=your_fernet_key_here
CELERY_BROKER_URL=redis://localhost:6379/0
```

---

## Notes

1. **Zoom API Developer Account**: Cần tạo Zoom App tại <https://marketplace.zoom.us/> để lấy Client ID/Secret
2. **Bot Account**: Cần 1 tài khoản Zoom Pro/Business cho bot
3. **Real-time features**: Cần Redis cho Channels và Celery
4. **Testing**: Mock Zoom API responses để test offline

---

# IMPLEMENTATION TODO: Internal Chat Room System (Zoom-like)

## Overview

Danh sách các task atomic để implement hệ thống Phòng Chat nội bộ dựa trên SYSTEM_DESIGN_REPORT.md v1.1.0

---

## Phase 1: Database Layer (Chat Room)

- [x] **CR-DB-001** | Database | Create `ChatRoom` model | `genmcq/models.py` ✅ 2026-01-06
- [x] **CR-DB-002** | Database | Create `ChatRoomMember` model | `genmcq/models.py` ✅ 2026-01-06
- [x] **CR-DB-003** | Database | Create `RoomMessage` model với thread support | `genmcq/models.py` ✅ 2026-01-06
- [x] **CR-DB-004** | Database | Create `RoomFile` model với extracted_text | `genmcq/models.py` ✅ 2026-01-06
- [x] **CR-DB-005** | Database | Create database migration | `python manage.py makemigrations` ✅ 2026-01-06
- [x] **CR-DB-006** | Database | Apply migration | `python manage.py migrate` ✅ 2026-01-06 (faked)

---

## Phase 2: Backend Layer (Chat Room)

### 2.1 Services

- [x] **CR-BE-001** | Backend | Create mock chatbot service | `genmcq/services/mock_chatbot.py` ✅ 2026-01-06
- [x] **CR-BE-002** | Backend | Implement keyword-based responses | `mock_chatbot.py` ✅ 2026-01-06
- [x] **CR-BE-003** | Backend | Implement bot commands (/help, /summary, /status) | `mock_chatbot.py` ✅ 2026-01-06
- [ ] **CR-BE-004** | Backend | Create file extraction service | `genmcq/services/file_extractor.py`

### 2.2 Views (Page Views)

- [x] **CR-BE-010** | Backend | Create room_list view (Dashboard) | `genmcq/views/room_views.py` ✅ 2026-01-06
- [x] **CR-BE-011** | Backend | Create room_create view | `genmcq/views/room_views.py` ✅ 2026-01-06
- [x] **CR-BE-012** | Backend | Create room_join view (password check) | `genmcq/views/room_views.py` ✅ 2026-01-06
- [x] **CR-BE-013** | Backend | Create room_chat view (main chat page) | `genmcq/views/room_views.py` ✅ 2026-01-06
- [x] **CR-BE-014** | Backend | Create room_leave view | `genmcq/views/room_views.py` ✅ 2026-01-06
- [x] **CR-BE-015** | Backend | Create room_settings view (host only) | `genmcq/views/room_views.py` ✅ 2026-01-06

### 2.3 API Views

- [x] **CR-BE-020** | Backend | Create room_messages_api (GET/POST) | `genmcq/views/room_api.py` ✅ 2026-01-06
- [ ] **CR-BE-021** | Backend | Create room_thread_api (GET thread replies) | `genmcq/views/room_api.py`
- [x] **CR-BE-022** | Backend | Create room_pin_message_api | `genmcq/views/room_api.py` ✅ 2026-01-06
- [x] **CR-BE-023** | Backend | Create room_members_api | `genmcq/views/room_api.py` ✅ 2026-01-06
- [x] **CR-BE-024** | Backend | Create room_typing_api | `genmcq/views/room_api.py` ✅ 2026-01-06
- [x] **CR-BE-025** | Backend | Create room_files_api (GET/POST/DELETE) | `genmcq/views/room_api.py` ✅ 2026-01-06
- [x] **CR-BE-026** | Backend | Create room_file_chat_api (RAG Mode) | `genmcq/views/room_api.py` ✅ 2026-01-06
- [x] **CR-BE-027** | Backend | Create room_bot_toggle_api | `genmcq/views/room_api.py` ✅ 2026-01-06
- [ ] **CR-BE-028** | Backend | Create room_bot_command_api | `genmcq/views/room_api.py`

### 2.4 URL Routes

- [x] **CR-BE-030** | Backend | Add room page URL routes | `genmcq/urls.py` ✅ 2026-01-06
- [x] **CR-BE-031** | Backend | Add room API URL routes | `genmcq/urls.py` ✅ 2026-01-06

### 2.5 Forms

- [x] **CR-BE-040** | Backend | Create RoomCreateForm | `genmcq/forms.py` ✅ 2026-01-06
- [x] **CR-BE-041** | Backend | Create RoomJoinForm (password) | `genmcq/forms.py` ✅ 2026-01-06
- [x] **CR-BE-042** | Backend | Create RoomSettingsForm | `genmcq/forms.py` ✅ 2026-01-06

### 2.6 Admin

- [x] **CR-BE-050** | Backend | Register ChatRoom in admin | `genmcq/admin.py` ✅ 2026-01-06
- [x] **CR-BE-051** | Backend | Register RoomMessage in admin | `genmcq/admin.py` ✅ 2026-01-06
- [x] **CR-BE-052** | Backend | Register RoomFile in admin | `genmcq/admin.py` ✅ 2026-01-06

---

## Phase 3: Frontend Layer (Chat Room)

### 3.1 Base Updates

- [x] **CR-FE-001** | Frontend | Add "Phòng Chat" link to navigation | `templates/base.html` ✅ 2026-01-06

### 3.2 Room Dashboard

- [x] **CR-FE-010** | Frontend | Create room list page (Dashboard) | `templates/zoom/rooms/list.html` ✅ 2026-01-06
- [x] **CR-FE-011** | Frontend | Add room card component | `templates/zoom/rooms/list.html` ✅ 2026-01-06
- [x] **CR-FE-012** | Frontend | Add filter/search UI | `templates/zoom/rooms/list.html` ✅ 2026-01-06
- [x] **CR-FE-013** | Frontend | Add recent rooms sidebar | `templates/zoom/rooms/list.html` ✅ 2026-01-06
- [x] **CR-FE-014** | Frontend | Add join password modal | `templates/zoom/rooms/list.html` ✅ 2026-01-06
- [x] **CR-FE-015** | Frontend | Create room form page | `templates/zoom/rooms/list.html` (modal) ✅ 2026-01-06

### 3.3 Chat Room Interface

- [x] **CR-FE-020** | Frontend | Create chat room page | `templates/zoom/rooms/chat.html` ✅ 2026-01-06
- [x] **CR-FE-021** | Frontend | Add message list UI | `templates/zoom/rooms/chat.html` ✅ 2026-01-06
- [ ] **CR-FE-022** | Frontend | Add thread view UI | `templates/zoom/rooms/chat.html` ⏳ Placeholder
- [x] **CR-FE-023** | Frontend | Add pinned messages section | `templates/zoom/rooms/chat.html` ✅ 2026-01-06
- [x] **CR-FE-024** | Frontend | Add members sidebar với status | `templates/zoom/rooms/chat.html` ✅ 2026-01-06
- [x] **CR-FE-025** | Frontend | Add file gallery sidebar | `templates/zoom/rooms/chat.html` ✅ 2026-01-06
- [x] **CR-FE-026** | Frontend | Add message input với mention/emoji | `templates/zoom/rooms/chat.html` ✅ 2026-01-06
- [x] **CR-FE-027** | Frontend | Add typing indicator | `templates/zoom/rooms/chat.html` ✅ 2026-01-06

### 3.4 File Chat (RAG Mode)

- [x] **CR-FE-030** | Frontend | Create file chat modal | `templates/zoom/rooms/chat.html` (modal) ✅ 2026-01-06
- [x] **CR-FE-031** | Frontend | Add file preview panel | `templates/zoom/rooms/chat.html` ✅ 2026-01-06
- [x] **CR-FE-032** | Frontend | Add chat panel | `templates/zoom/rooms/chat.html` ✅ 2026-01-06

### 3.5 JavaScript

- [x] **CR-FE-040** | Frontend | Create room chat JS handler | `static/js/room_chat.js` ✅ 2026-01-06
- [x] **CR-FE-041** | Frontend | Implement message polling (2s interval) | `static/js/room_chat.js` ✅ 2026-01-06
- [ ] **CR-FE-042** | Frontend | Implement file upload with progress | `static/js/room_chat.js`
- [x] **CR-FE-043** | Frontend | Implement typing indicator | `static/js/room_chat.js` ✅ 2026-01-06
- [x] **CR-FE-044** | Frontend | Implement mention autocomplete | `static/js/room_chat.js` ✅ 2026-01-06
- [x] **CR-FE-045** | Frontend | Implement bot toggle button | `static/js/room_chat.js` ✅ 2026-01-06
- [ ] **CR-FE-046** | Frontend | Create file chat JS handler | `static/js/file_chat.js`

---

## Phase 4: Testing (Chat Room)

- [ ] **CR-TST-001** | Testing | Test ChatRoom model | `genmcq/tests/test_room_models.py`
- [ ] **CR-TST-002** | Testing | Test room creation flow | Manual
- [ ] **CR-TST-003** | Testing | Test join room with password | Manual
- [ ] **CR-TST-004** | Testing | Test chat messages | Manual
- [ ] **CR-TST-005** | Testing | Test file upload | Manual
- [ ] **CR-TST-006** | Testing | Test bot toggle | Manual
- [ ] **CR-TST-007** | Testing | Test RAG file chat | Manual
- [ ] **CR-TST-008** | Testing | Test member status display | Manual

---

## Implementation Order (Chat Room)

```
Phase 1: Database (CR-DB-001 → CR-DB-006)
    ↓
Phase 2.1: Services (CR-BE-001 → CR-BE-004)
    ↓
Phase 2.2-2.3: Views & API (CR-BE-010 → CR-BE-028)
    ↓
Phase 2.4-2.6: Routes, Forms, Admin (CR-BE-030 → CR-BE-052)
    ↓
Phase 3.1-3.2: Base & Dashboard UI (CR-FE-001 → CR-FE-015)
    ↓
Phase 3.3-3.4: Chat Room & File Chat UI (CR-FE-020 → CR-FE-032)
    ↓
Phase 3.5: JavaScript (CR-FE-040 → CR-FE-046)
    ↓
Phase 4: Testing (CR-TST-001 → CR-TST-008)
```

---

## Mock Data (chatbot_responses.json)

```json
{
  "responses": {
    "chào bot": "Chào bạn! Tôi là trợ lý ảo của phòng.",
    "/help": "Các lệnh: /summary, /status, @bot + câu hỏi",
    "/summary": "📝 15 tin nhắn trong 1 giờ qua",
    "/status": "📊 5 thành viên online, 2 file mới",
    "default": "Đây là câu trả lời mẫu từ chatbot."
  },
  "welcome_message": "🤖 Bot đã tham gia! Gõ /help để xem lệnh.",
  "new_member_message": "👋 Chào mừng {username}!"
}
```

---

## Notes (Chat Room)

1. **Polling vs WebSocket**: Dùng polling 2s cho đơn giản, có thể upgrade lên WebSocket sau
2. **File extraction**: Dùng PyPDF2 cho PDF, python-docx cho DOCX
3. **Mock chatbot**: Keyword matching, có thể integrate Gemini AI sau
4. **Permissions**: Check role trước mỗi action (host/moderator/member)
