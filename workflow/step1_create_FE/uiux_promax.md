---
name: ui-ux-pro-max
description: 'UI/UX workflow for HTML + Tailwind CSS + JavaScript projects'
agent: 'agent'
---

# ui-ux-pro-max

Comprehensive UI/UX workflow for Django + Tailwind CSS + JavaScript projects. Includes system analysis, requirements extraction from design documents, and backend specs generation.

**Tech Stack:** `HTML5` + `Tailwind CSS` + `Vanilla JS` + `Django Templates`

---

## ⛔ CRITICAL: MANDATORY CODE EXECUTION DIRECTIVE

> **🚨 YOU MUST WRITE ACTUAL CODE FILES - NOT JUST PLANNING DOCUMENTS! 🚨**

```
╔═══════════════════════════════════════════════════════════════════════════════╗
║                         ⚠️  FORBIDDEN BEHAVIORS  ⚠️                           ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ❌ DO NOT create implementation_plan.md artifacts                           ║
║  ❌ DO NOT create task.md or todo.md artifacts                               ║
║  ❌ DO NOT create BACKEND_SPECS.md as final output                           ║
║  ❌ DO NOT stop after "creating a plan" - EXECUTE THE PLAN!                  ║
║  ❌ DO NOT ask user to "approve the plan" before coding                      ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝

╔═══════════════════════════════════════════════════════════════════════════════╗
║                         ✅  MANDATORY BEHAVIORS  ✅                           ║
╠═══════════════════════════════════════════════════════════════════════════════╣
║                                                                               ║
║  ✅ USE write_to_file tool to CREATE template files (.html)                  ║
║  ✅ USE write_to_file tool to CREATE JavaScript files (.js)                  ║
║  ✅ USE write_to_file tool to CREATE CSS files (.css)                        ║
║  ✅ USE replace_file_content tool to MODIFY existing files                   ║
║  ✅ WRITE complete, working, production-ready code                           ║
║  ✅ ONLY create FRONTEND_WORK_REPORT.md AFTER all code is written            ║
║                                                                               ║
╚═══════════════════════════════════════════════════════════════════════════════╝
```

### Execution Order (MUST FOLLOW)

```yaml
execution_steps:
  1_read_requirements:
    - Read IMPLEMENTATION_TODO.md Phase 3 tasks
    - Read SYSTEM_DESIGN_REPORT.md for context
    - Identify which files to create/modify
    
  2_analyze_existing:
    - View existing templates/base.html
    - View existing templates/components/
    - Understand current design patterns
    
  3_WRITE_CODE (THIS IS THE MAIN WORK):
    - FOR EACH task in Phase 3 (FE-xxx):
        - USE write_to_file to CREATE the template file
        - USE write_to_file to CREATE any supporting JS/CSS
        - USE replace_file_content to UPDATE navigation/base
    - This step should produce ACTUAL FILES in templates/ and static/
    
  4_document_work:
    - ONLY after all code is written
    - Create FRONTEND_WORK_REPORT.md documenting what was done
```

### Verification Checklist (Before Completion)

```markdown
□ Did I CREATE at least one .html file using write_to_file? 
□ Did I CREATE or MODIFY at least one .js file?
□ Did I UPDATE base.html or navigation for new pages?
□ Are all templates in templates/{app_name}/ directory?
□ Is the code complete and runnable (not placeholder)?

If ANY answer is NO → GO BACK AND WRITE THE CODE!
```

---

## CRITICAL: Build Mode Detection

```
┌─────────────────────────────────────────────────────────────────┐
│                    DECISION FLOWCHART                           │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│              Is this a NEW project or EXISTING system?          │
│                          │                                      │
│              ┌───────────┴───────────┐                          │
│              │                       │                          │
│              ▼                       ▼                          │
│         NEW PROJECT            EXISTING SYSTEM                  │
│              │                       │                          │
│              ▼                       ▼                          │
│     ╔═══════════════════╗   ╔═══════════════════════╗          │
│     ║ FULL BUILD MODE   ║   ║ INCREMENTAL MODE      ║          │
│     ╠═══════════════════╣   ╠═══════════════════════╣          │
│     ║ 1. Start from     ║   ║ 1. Analyze existing   ║          │
│     ║    scratch        ║   ║    templates/pages    ║          │
│     ║                   ║   ║                       ║          │
│     ║ 2. Create all     ║   ║ 2. Match existing     ║          │
│     ║    components     ║   ║    design patterns    ║          │
│     ║                   ║   ║                       ║          │
│     ║ 3. Full design    ║   ║ 3. Only add/modify    ║          │
│     ║    system         ║   ║    what's needed      ║          │
│     ╚═══════════════════╝   ╚═══════════════════════╝          │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Prerequisites

Check if Python is installed:

```bash
python3 --version || python --version
```

If Python is not installed, install it based on user's OS:

**macOS:**

```bash
brew install python3
```

**Ubuntu/Debian:**

```bash
sudo apt update && sudo apt install python3
```

**Windows:**

```powershell
winget install Python.Python.3.12
```

---

## WORKFLOW

### Step 0: System Analysis (REQUIRED FIRST)

> ⚠️ Before ANY design work, analyze what already exists!

#### 0.1 Check for Existing System Report

```yaml
check_for_existing_docs:
  - Read: workflow/step0_design/SYSTEM_DESIGN_REPORT.md
  - If exists: Extract frontend-related info (templates, components, styles)
  - If not exists: Proceed to scan codebase
```

#### 0.2 Analyze Existing Frontend (If SYSTEM_DESIGN_REPORT.md not available)

```yaml
scan_existing_frontend:
  templates:
    path: "templates/**/*.html"
    capture:
      - Template hierarchy (base.html → child templates)
      - Existing components (navbar, footer, cards, forms)
      - CSS classes used (Tailwind patterns)
      - JavaScript files included
      
  static_assets:
    path: "static/**/*"
    capture:
      - CSS files and variables
      - JavaScript modules
      - Image assets
      - Icon libraries used
      
  design_patterns:
    capture:
      - Color scheme (primary, secondary, accent)
      - Typography (font families, sizes)
      - Spacing system (margins, paddings)
      - Component patterns (cards, buttons, forms)
```

#### 0.3 Generate Existing System Summary

Output format:

```markdown
## Existing Frontend Analysis

### Templates Structure
| Template | Extends | Purpose | Key Components |
|----------|---------|---------|----------------|
| base.html | - | Layout wrapper | Navbar, Footer, Scripts |
| home.html | base.html | Landing page | Hero, Features, CTA |

### Existing Components
| Component | Location | Usage |
|-----------|----------|-------|
| Navbar | templates/components/navbar.html | All pages |
| Card | inline in templates | MCQ display, history items |

### Design Tokens (Current)
| Token | Value | Usage |
|-------|-------|-------|
| Primary Color | #3B82F6 (blue-500) | Buttons, links |
| Background | #F8FAFC (slate-50) | Page background |
| Font Family | Inter, system-ui | All text |

### Dependencies
- Tailwind CSS v3.x
- Heroicons
- AlpineJS (if used)

### Missing/Needs Improvement
- No dark mode support
- Inconsistent button styles
- No loading states
```

---

### Step 1: Extract Frontend Requirements

#### 1.1 From User Request

```yaml
extract_from_request:
  pages_needed:
    - List all pages mentioned or implied
    - Example: "Zoom management" → list, create, join, detail pages
    
  components_needed:
    - UI components required
    - Forms, tables, modals, cards, etc.
    
  interactions:
    - User flows and interactions
    - Real-time updates, notifications
    
  responsive_requirements:
    - Mobile-first or desktop-first
    - Specific breakpoints mentioned
```

#### 1.2 From Reference Websites (if provided)

```yaml
extract_from_references:
  layout_patterns:
    - Navigation style (sidebar, topbar, hybrid)
    - Content layout (grid, list, masonry)
    - Page structure (hero, sections, footer)
    
  visual_design:
    - Color palette estimation
    - Typography style (serif, sans-serif, display)
    - Iconography style
    - Illustration/image usage
    
  interactions:
    - Hover effects
    - Animations/transitions
    - Loading patterns
    - Micro-interactions
    
  component_patterns:
    - Card designs
    - Form layouts
    - Button styles
    - Table/list designs
```

#### 1.3 From Design Documents (PRIMARY SOURCE)

> ⚠️ **REQUIRED**: Always check these files first before starting any UI work!

**File Priority Order:**

1. `IMPLEMENTATION_TODO.md` - Contains specific frontend tasks (Phase 3)
2. `SYSTEM_DESIGN_REPORT.md` - Contains context (models, APIs, data flow)

```yaml
extract_from_implementation_todo:
  file: "./workflow/step0_design/IMPLEMENTATION_TODO.md"
  
  extract_phase_3:
    # Look for "## Phase 3: Frontend Layer" section
    tasks:
      - Task IDs (FE-001, FE-002, ...)
      - Task descriptions
      - Target file paths (templates/, static/, etc.)
      - Dependencies on other phases
    
  example_extraction: |
    From IMPLEMENTATION_TODO.md:
    - [ ] **FE-020** | Frontend | Create meetings list page | `templates/zoom/meetings/list.html`
    - [ ] **FE-021** | Frontend | Create meeting form | `templates/zoom/meetings/create.html`
    
    → Extract:
      pages_to_create:
        - templates/zoom/meetings/list.html (FE-020)
        - templates/zoom/meetings/create.html (FE-021)
      
  extract_dependencies:
    # Look for backend tasks that frontend depends on
    - API endpoints from Phase 2 (BE-050, BE-051, ...)
    - Models from Phase 1 (DB-001, DB-002, ...)
```

```yaml
extract_from_system_design:
  file: "./workflow/step0_design/SYSTEM_DESIGN_REPORT.md"
  
  extract_context:
    # Understand WHAT data to display
    database_models:
      - Field names and types
      - Relationships between models
      - Required vs optional fields
      
    api_endpoints:
      - Endpoint URLs
      - Request/response structure
      - Authentication requirements
      
    navigation_structure:
      - Menu items to add
      - Page hierarchy
      
    data_flow:
      - How data flows from API to UI
      - Real-time requirements
      
  example_extraction: |
    From SYSTEM_DESIGN_REPORT.md:
    ### ZoomMeeting Model:
    - topic: CharField
    - scheduled_at: DateTime
    - status: enum (scheduled, active, ended)
    
    → Extract for UI:
      meeting_card_display:
        - title: meeting.topic
        - date: format(meeting.scheduled_at)
        - badge: status (color-coded)
```

**Minimum Requirements Checklist:**

```markdown
Before starting UI work, confirm you have extracted:

□ Phase 3 tasks from IMPLEMENTATION_TODO.md
  - [ ] List of pages to create
  - [ ] List of components to build
  - [ ] File paths for each task
  
□ Context from SYSTEM_DESIGN_REPORT.md
  - [ ] Models and their fields
  - [ ] API endpoints and responses
  - [ ] Navigation structure updates
  
□ Dependencies identified
  - [ ] Which backend APIs are needed
  - [ ] Which models must exist first
```

---

### Step 2: Generate Backend Support Report

> 📋 This section creates specs that help backend developers

#### 2.1 Data Schema Requirements (for Backend)

```markdown
## Frontend Data Requirements

### Page: Meeting List
| Data Field | Type | Source | Notes |
|------------|------|--------|-------|
| meetings | Array<Meeting> | API: GET /api/zoom/meetings/ | Paginated, sorted by date |
| meeting.id | UUID | - | For routing |
| meeting.topic | String | - | Display title |
| meeting.scheduled_at | DateTime | - | Format: "Today, 2:30 PM" |
| meeting.status | Enum | - | Show badge: scheduled/active/ended |
| meeting.participants_count | Integer | - | Show "5 participants" |

### Page: Meeting Create Form
| Field | Type | Validation | Default |
|-------|------|------------|---------|
| topic | String | Required, max 200 chars | - |
| scheduled_at | DateTime | Required, must be future | Now + 1 hour |
| duration_minutes | Integer | 15-480 | 60 |
| password | String | Optional, min 6 chars | Auto-generated |
| waiting_room | Boolean | - | true |
```

#### 2.2 API Requirements (for Backend)

```markdown
## API Endpoints Required by Frontend

### Meeting Management
| Method | Endpoint | Purpose | Request Body | Response |
|--------|----------|---------|--------------|----------|
| GET | /api/zoom/meetings/ | List meetings | - | { meetings: [], pagination } |
| POST | /api/zoom/meetings/ | Create meeting | { topic, scheduled_at, ... } | { meeting } |
| GET | /api/zoom/meetings/{id}/ | Get details | - | { meeting, participants } |
| DELETE | /api/zoom/meetings/{id}/ | Delete | - | 204 No Content |

### Required Response Fields
\`\`\`json
{
  "id": "uuid",
  "topic": "string",
  "scheduled_at": "ISO8601",
  "join_url": "string",     // For "Join Meeting" button
  "host_url": "string",     // For "Start Meeting" button (host only)
  "status": "scheduled|active|ended"
}
\`\`\`
```

#### 2.3 State Management Requirements

```markdown
## Frontend State Requirements

### Global State
| State | Type | Persisted | Purpose |
|-------|------|-----------|---------|
| user | User | localStorage | Current user info |
| credits | Integer | - | Show in navbar, update after actions |
| theme | "light" | "dark" | localStorage | Dark mode preference |

### Page-specific State
| Page | State | Source | Update Trigger |
|------|-------|--------|----------------|
| Meeting List | meetings[] | API | On mount, after create/delete |
| Meeting Detail | meeting, participants[] | API | Polling every 10s if active |
```

---

### Step 3: Design Reference Search

Use `search.py` to gather design information:

```bash
python workflow/step1_create_FE/uiux_promax/scripts/search.py "<keyword>" --domain <domain> [-n <max_results>]
```

**Recommended search order:**

1. **Product** - Get style recommendations for product type
2. **Style** - Get detailed style guide (colors, effects, frameworks)
3. **Typography** - Get font pairings with Google Fonts imports
4. **Color** - Get color palette (Primary, Secondary, CTA, Background, Text, Border)
5. **Landing** - Get page structure (if landing page)
6. **Chart** - Get chart recommendations (if dashboard/analytics)
7. **UX** - Get best practices and anti-patterns
8. **Guidelines** - Get Tailwind + JS best practices

### Available Domains

| Domain | Use For | Example Keywords |
|--------|---------|------------------|
| `product` | Product type recommendations | SaaS, e-commerce, portfolio, healthcare, beauty |
| `style` | UI styles, colors, effects | glassmorphism, minimalism, dark mode, brutalism |
| `typography` | Font pairings, Google Fonts | elegant, playful, professional, modern |
| `color` | Color palettes by product type | saas, ecommerce, healthcare, beauty, fintech |
| `landing` | Page structure, CTA strategies | hero, hero-centric, testimonial, pricing |
| `chart` | Chart types, library recommendations | trend, comparison, timeline, funnel |
| `ux` | Best practices, anti-patterns | animation, accessibility, z-index, loading |
| `prompt` | AI prompts, CSS keywords | (style name) |

### Tech Stack (Fixed)

> 🛠️ This project uses a fixed stack. No framework selection needed.

| Layer | Technology | Notes |
|-------|------------|-------|
| **Structure** | HTML5 | Semantic elements, accessibility |
| **Styling** | Tailwind CSS | Utility-first, responsive, dark mode |
| **Interactivity** | Vanilla JavaScript | Alpine.js optional for reactivity |
| **Icons** | Heroicons / Lucide | SVG icons only, no emoji |
| **Templating** | Django Templates | Extends base.html pattern |

---

### Step 4: IMPLEMENTATION - WRITE THE CODE (CRITICAL!)

> ⚠️ **THIS IS WHERE YOU ACTUALLY CREATE/MODIFY FILES - NOT JUST PLAN!**

#### 4.0 Code Execution Checklist

```yaml
before_writing_code:
  confirm:
    - [ ] I have the extracted requirements from Step 1
    - [ ] I know which files to create/modify from IMPLEMENTATION_TODO.md
    - [ ] I understand the data models from SYSTEM_DESIGN_REPORT.md
    - [ ] I have analyzed existing patterns (if Incremental Mode)
```

---

#### 4.1 Create/Modify Template Files (DO THIS!)

> 🔧 **Execute these actions using write_to_file and replace_file_content tools**

**For EACH page/template in your task list:**

```yaml
action: CREATE or MODIFY template file
file: templates/{app}/{page_name}.html

steps:
  1. Create the file with proper Django template structure
  2. Extend base.html if exists
  3. Add all HTML with Tailwind classes
  4. Include all required blocks (title, content, scripts)
  5. Add Alpine.js/JS for interactivity if needed
```

**Example Template Structure:**

```html
{% extends "base.html" %}
{% load static %}

{% block title %}{Page Title}{% endblock %}

{% block content %}
<div class="container mx-auto px-4 py-8">
    
    <!-- Page Header -->
    <div class="flex justify-between items-center mb-8">
        <h1 class="text-3xl font-bold text-gray-900">{Page Title}</h1>
        <a href="{% url '{app}:{action}' %}" 
           class="bg-blue-600 hover:bg-blue-700 text-white px-4 py-2 rounded-lg">
            {Action Button}
        </a>
    </div>
    
    <!-- Main Content -->
    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">
        {% for item in items %}
        <div class="bg-white rounded-xl shadow-sm border p-6 hover:shadow-lg transition">
            <h3 class="font-semibold text-lg">{{ item.title }}</h3>
            <p class="text-gray-600 mt-2">{{ item.description }}</p>
        </div>
        {% empty %}
        <div class="col-span-full text-center py-12 text-gray-500">
            No items found
        </div>
        {% endfor %}
    </div>
    
</div>
{% endblock %}

{% block extra_js %}
<script>
    // Page-specific JavaScript
</script>
{% endblock %}
```

---

#### 4.2 Create/Modify Component Files (DO THIS!)

**For EACH component needed:**

```yaml
action: CREATE component file
file: templates/components/{component_name}.html

# Component should be reusable with Django include tag
# {% include "components/card.html" with item=meeting %}
```

---

#### 4.3 Create/Modify JavaScript Files (DO THIS!)

```yaml
action: CREATE or MODIFY JavaScript file  
file: static/js/{feature_name}.js

content_includes:
  - Event listeners for user interactions
  - AJAX calls to API endpoints
  - Form validation logic
  - Dynamic UI updates
  - Error handling with user feedback
```

**JavaScript Template:**

```javascript
// {feature_name}.js - {Description}

document.addEventListener('DOMContentLoaded', function() {
    
    // DOM Elements
    const form = document.getElementById('{form-id}');
    const container = document.getElementById('{container-id}');
    
    // Event Listeners
    if (form) {
        form.addEventListener('submit', handleSubmit);
    }
    
    // Functions
    async function handleSubmit(e) {
        e.preventDefault();
        
        const formData = new FormData(form);
        const btn = form.querySelector('button[type="submit"]');
        
        try {
            btn.disabled = true;
            btn.innerHTML = '<span class="animate-spin">⏳</span> Loading...';
            
            const response = await fetch(form.action, {
                method: 'POST',
                body: formData,
                headers: {
                    'X-CSRFToken': document.querySelector('[name=csrfmiddlewaretoken]').value
                }
            });
            
            if (!response.ok) throw new Error('Request failed');
            
            const data = await response.json();
            // Handle success
            
        } catch (error) {
            console.error('Error:', error);
            showToast('An error occurred', 'error');
        } finally {
            btn.disabled = false;
            btn.innerHTML = 'Submit';
        }
    }
    
    function showToast(message, type = 'info') {
        // Toast notification
    }
});
```

---

#### 4.4 Update CSS/Styles (DO THIS if needed!)

```yaml
action: MODIFY existing CSS or CREATE custom styles
file: static/css/{app}.css or inline in templates

when_needed:
  - Custom animations not in Tailwind
  - Complex gradients or effects
  - Override third-party library styles
```

---

#### 4.5 Update Navigation (DO THIS if new pages added!)

```yaml
action: MODIFY navigation component
file: templates/components/navbar.html OR templates/base.html

add:
  - New menu items for new pages
  - Active state detection
  - Mobile menu updates
```

---

#### 4.6 Implementation Order

```yaml
order:
  1. Base layout changes (if any) → templates/base.html
  2. Reusable components → templates/components/
  3. Page templates → templates/{app}/
  4. JavaScript functionality → static/js/
  5. Any custom CSS → static/css/
  6. Navigation updates → navbar/sidebar
  
after_each_file:
  - Verify syntax is correct
  - Ensure all {% url %} tags use correct names
  - Check all static files use {% static %}
```

---

#### 4.7 Incremental Mode Checklist

```yaml
if_incremental_mode:
  rules:
    - [ ] Extend existing base.html - DO NOT create new base
    - [ ] Match existing component visual patterns exactly
    - [ ] Use same Tailwind class conventions as existing pages
    - [ ] Follow same JavaScript patterns (Alpine vs Vanilla)
    - [ ] Maintain consistent design tokens (colors, spacing)
```

#### 4.8 Full Build Mode Checklist

```yaml
if_full_build_mode:
  rules:
    - [ ] Create base.html with complete layout
    - [ ] Build all required components from scratch
    - [ ] Establish design system documentation
    - [ ] Create comprehensive navigation structure
```

---

### Step 5: Generate Work Report (SINGLE SOURCE OF TRUTH)

> 📝 Create `FRONTEND_WORK_REPORT.md` - This is the ONLY file the review step needs to read!

**Output Path:** `./workflow/step1_create_FE/FRONTEND_WORK_REPORT.md`

> ⚠️ **IMPORTANT:** This file must contain ALL context extracted from design docs so that the review step doesn't need to read multiple files.

```markdown
# Frontend Work Report

**Date:** YYYY-MM-DD
**Feature:** [Feature Name]
**Build Mode:** Full Build | Incremental

---

## Part 1: Extracted Requirements (from Design Docs)

> This section is copied from IMPLEMENTATION_TODO.md and SYSTEM_DESIGN_REPORT.md at the START of FE work.

### 1.1 Assigned Tasks (from IMPLEMENTATION_TODO.md Phase 3)

| Task ID | Description | Target File | Status |
|---------|-------------|-------------|--------|
| FE-001 | Create meeting list page | templates/zoom/list.html | ⏳ Pending |
| FE-002 | Create meeting form | templates/zoom/create.html | ⏳ Pending |
| FE-003 | Add meeting card component | templates/components/card.html | ⏳ Pending |

### 1.2 Required Data Models (from SYSTEM_DESIGN_REPORT.md)

```yaml
ZoomMeeting:
  fields:
    - id: UUID
    - topic: CharField (max 255)
    - scheduled_at: DateTime
    - status: Enum [scheduled, active, ended]
    - join_url: URLField
    - participants_count: Integer
  display_mapping:
    - Card title: topic
    - Card subtitle: formatted scheduled_at
    - Card badge: status (color-coded)
```

### 1.3 Required API Endpoints (from SYSTEM_DESIGN_REPORT.md)

| Method | Endpoint | Purpose | Response Fields |
|--------|----------|---------|-----------------|
| GET | /api/zoom/meetings/ | List meetings | id, topic, scheduled_at, status |
| POST | /api/zoom/meetings/ | Create meeting | id, join_url |
| DELETE | /api/zoom/meetings/{id}/ | Delete meeting | 204 |

### 1.4 Navigation Updates (from SYSTEM_DESIGN_REPORT.md)

```yaml
add_to_navbar:
  - label: "Zoom"
    url: "/zoom/"
    icon: "video-camera"
    children:
      - Meetings: "/zoom/meetings/"
      - Create: "/zoom/meetings/create/"
```

---

## Part 2: Work Completed

### 2.1 Summary

Brief description of what was built/modified.

### 2.2 Task Completion Status

| Task ID | Description | Target File | Status | Notes |
|---------|-------------|-------------|--------|-------|
| FE-001 | Create meeting list page | templates/zoom/list.html | ✅ Done | - |
| FE-002 | Create meeting form | templates/zoom/create.html | ✅ Done | - |
| FE-003 | Add meeting card component | templates/components/card.html | ❌ Skipped | Inline in list.html |

### 2.3 Files Created

| File | Purpose | Lines |
|------|---------|-------|
| templates/zoom/list.html | Meeting list page | 150 |
| static/js/zoom.js | Meeting interactions | 80 |

### 2.4 Files Modified

| File | Changes | Reason |
|------|---------|--------|
| templates/base.html | Added Zoom nav link | Navigation update |

### 2.5 Components Built

| Component | Location | Reusable |
|-----------|----------|----------|
| MeetingCard | templates/zoom/list.html (inline) | No |

---

## Part 3: Design Decisions & Notes

### 3.1 Key Decisions

| Decision | Rationale |
|----------|-----------|
| Used modal for join | Faster UX than separate page |
| Green for "active" status | Consistent with existing success color |

### 3.2 New Features Added (Not in Original Spec)

| Feature | Location | Reason | Priority |
|---------|----------|--------|----------|
| Meeting search | list.html | UX improvement for many meetings | Medium |

### 3.3 Dependencies on Backend

| Endpoint | Status | Blocking? |
|----------|--------|-----------|
| GET /api/zoom/meetings/ | ⏳ Not implemented | Yes |
| POST /api/zoom/meetings/ | ⏳ Not implemented | Yes |

---

## Part 4: Testing Status

### 4.1 Responsive Testing

| Breakpoint | Width | Status |
|------------|-------|--------|
| Mobile | 320px | ✅ Pass |
| Tablet | 768px | ✅ Pass |
| Desktop | 1440px | ✅ Pass |

### 4.2 Functionality Testing

| Test | Status | Notes |
|------|--------|-------|
| Page loads without errors | ✅ | - |
| Navigation works | ✅ | - |
| Form submits | ⏳ | Blocked by API |

### 4.3 Accessibility

- [x] All images have alt text
- [x] Form inputs have labels
- [x] Focus states visible

---

## Part 5: For Backend Team

### 5.1 API Specification Needed

\`\`\`json
// GET /api/zoom/meetings/
// Response:
{
  "meetings": [
    {
      "id": "uuid",
      "topic": "string",
      "scheduled_at": "ISO8601",
      "status": "scheduled|active|ended",
      "join_url": "string"
    }
  ],
  "pagination": { "page": 1, "total": 10 }
}
\`\`\`

### 5.2 Form Fields to Validate

| Field | Type | Validation |
|-------|------|------------|
| topic | String | Required, max 200 |
| scheduled_at | DateTime | Required, must be future |

```



---

## Common UI Rules

### Icons & Visual Elements

| Rule | Do | Don't |
|------|----|----- |
| **No emoji icons** | Use SVG icons (Heroicons, Lucide) | Use emojis like 🎨 🚀 as UI icons |
| **Stable hover states** | Use color/opacity transitions | Use scale transforms that shift layout |
| **Correct brand logos** | Research official SVG | Guess or use incorrect paths |

### Interaction & Cursor

| Rule | Do | Don't |
|------|----|----- |
| **Cursor pointer** | Add `cursor-pointer` to all clickable | Leave default cursor |
| **Hover feedback** | Provide visual feedback | No indication element is interactive |
| **Smooth transitions** | Use `transition-colors duration-200` | Instant or too slow (>500ms) |

### Light/Dark Mode

| Rule | Do | Don't |
|------|----|----- |
| **Glass card light mode** | Use `bg-white/80` or higher | Use `bg-white/10` (too transparent) |
| **Text contrast light** | Use `#0F172A` (slate-900) | Use `#94A3B8` (slate-400) |

### Layout & Spacing

| Rule | Do | Don't |
|------|----|----- |
| **Floating navbar** | Add `top-4 left-4 right-4` spacing | Stick to `top-0 left-0 right-0` |
| **Content padding** | Account for fixed navbar height | Let content hide behind fixed elements |

---

## Pre-Delivery Checklist

### Visual Quality

- [ ] No emojis used as icons (use SVG instead)
- [ ] All icons from consistent icon set
- [ ] Hover states don't cause layout shift
- [ ] Matches existing design patterns (if incremental)

### Interaction

- [ ] All clickable elements have `cursor-pointer`
- [ ] Transitions are smooth (150-300ms)
- [ ] Focus states visible for keyboard navigation

### Light/Dark Mode

- [ ] Light mode text has sufficient contrast
- [ ] Borders visible in both modes
- [ ] Test both modes before delivery

### Layout

- [ ] Responsive at 320px, 768px, 1024px, 1440px
- [ ] No horizontal scroll on mobile
- [ ] No content hidden behind fixed elements

### Accessibility

- [ ] All images have alt text
- [ ] Form inputs have labels
- [ ] `prefers-reduced-motion` respected

### Documentation

- [ ] FRONTEND_WORK_REPORT.md created
- [ ] All new/modified files listed
- [ ] Backend requirements documented
- [ ] New features identified and noted

---

## Output Files

This workflow generates:

| File | Purpose | Location |
|------|---------|----------|
| `FRONTEND_WORK_REPORT.md` | Work documentation & review | `./workflow/step1_create_FE/` |
| Template files | Actual UI pages | `./templates/{feature}/` |
| Component files | Reusable components | `./templates/components/` |
| CSS/JS files | Styles and interactions | `./static/{css,js}/` |
