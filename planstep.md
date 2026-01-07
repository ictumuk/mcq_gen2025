# Plan: Convert ZoomChat Styling to MCQ System Theme

## Objective
Convert all Tailwind CSS code of ZoomChat (`list.html`, `chat.html`) to match the styling of the MCQ system (`generate_mcq.html`, `input.css`). Specifically, update the Zoom list to display as a single vertically stacked list.

## Tasks

### 1. Analyze & Prepare
- [x] Review `templates/generate_mcq.html` and `static/src/input.css` for design tokens (gradients: `from-blue-600 to-purple-600`, shadows, rounded corners).
- [x] Review `templates/zoom/rooms/list.html` and `templates/zoom/rooms/chat.html`.

### 2. Refactor Zoom Room List (`templates/zoom/rooms/list.html`)
- [ ] **Layout Change:** Convert grid layout (`grid-cols-1 md:grid-cols-3`) to a vertical stack (`flex flex-col space-y-4`).
- [ ] **Card Design:** Redesign room cards to be horizontal rows:
    -   **Left:** Room Icon (using MCQ gradient background).
    -   **Middle:** Room Name, Description, Tags (Type).
    -   **Right:** Stats (Members, Online), Action Buttons (Join).
- [ ] **Styling:** Apply MCQ-specific shadow classes (`shadow-lg`, `shadow-blue-500/30` for actions) and borders.
- [ ] **Script Update:** Ensure the client-side search functionality (`document.querySelectorAll`) works with the new DOM structure.

### 3. Refactor Zoom Chat Interface (`templates/zoom/rooms/chat.html`)
- [ ] **Theme consistency:** Update gradients to match `from-blue-600 to-purple-600`.
- [ ] **Input Area:** Style the message input to match `input-animated` and `focus:ring-blue-500` from MCQ forms.
- [ ] **Sidebar:** Ensure the sidebar (Members/Files) uses the same border and background conventions as MCQ panels.
- [ ] **Buttons:** Update "Send", "Upload", and "Toggle Bot" buttons to use the standard MCQ gradient buttons.

### 4. Backend & JavaScript Assessment
- [ ] **Backend (`views.py`):** 
    -   *Current Assessment:* No immediate backend changes required for styling. The `rooms` context variable provides sufficient data (`name`, `description`, `room_type`, `member_count`, `online_count`).
    -   *Potential Enhancement:* If the list view requires "Last Message" or "Last Active" sorting, backend updates would be needed. For now, we proceed with existing data.
- [ ] **JavaScript:**
    -   `list.html`: Search script needs to target the correct elements in the new list layout.
    -   `chat.html`: Alpine.js logic should remain functional, but class bindings might need updates if class names change significantly.

## Execution Order
1.  Modify `templates/zoom/rooms/list.html`.
2.  Modify `templates/zoom/rooms/chat.html`.
3.  Verify responsiveness and dark mode.