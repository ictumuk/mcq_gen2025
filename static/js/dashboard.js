/**
 * Dashboard Controller
 * Handles dashboard-specific functionality
 */

// API Configuration for dashboard
const DASHBOARD_API_ENDPOINTS = {
    getQuestions: '/api/questions/'
};

// Get CSRF token from cookies
function getCsrfToken() {
    const name = 'csrftoken';
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

// Escape HTML to prevent XSS
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Toast Notification
 */
function showToast(message, type = 'info') {
    // Remove existing toasts
    const existingToasts = document.querySelectorAll('.toast-notification');
    existingToasts.forEach(t => {
        t.style.opacity = '0';
        t.style.transform = 'translateX(100%)';
        setTimeout(() => t.remove(), 200);
    });

    const toast = document.createElement('div');
    toast.className = 'toast-notification fixed top-20 right-4 z-50 flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg transition-all duration-300';
    
    const colors = {
        success: 'bg-green-500 text-white shadow-green-500/30',
        error: 'bg-red-500 text-white shadow-red-500/30',
        warning: 'bg-yellow-500 text-white shadow-yellow-500/30',
        info: 'bg-blue-500 text-white shadow-blue-500/30'
    };
    toast.className += ' ' + (colors[type] || colors.info);

    const icons = {
        success: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>',
        error: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>',
        warning: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>',
        info: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>'
    };

    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';

    toast.innerHTML = `
        <svg class="w-5 h-5 flex-shrink-0" fill="none" stroke="currentColor" viewBox="0 0 24 24">
            ${icons[type] || icons.info}
        </svg>
        <span class="text-sm font-medium">${escapeHtml(message)}</span>
        <button onclick="closeToast(this.parentElement)" class="ml-2 hover:opacity-70 transition-opacity">
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
        </button>
    `;

    document.body.appendChild(toast);

    // Animate in
    requestAnimationFrame(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    });

    // Auto remove after 4 seconds
    setTimeout(() => closeToast(toast), 4000);
}

function closeToast(toast) {
    if (!toast || !toast.parentElement) return;
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
}

/**
 * Normalize text for display: convert <br> to newline
 */
function formatDisplayText(text) {
    if (!text) return '';
    return String(text).replace(/<br\s*\/?>/gi, '\n');
}

/**
 * Create Question Card HTML for display in modal (read-only)
 */
function createQuestionCardHTML(question, orderNum, difficultyLabel) {
    const rawContent = question.stem || question.content || '';
    const displayContent = formatDisplayText(rawContent);
    const hasCode = /```|`|<code>|<pre>/i.test(rawContent);
    const stemExtraClass = hasCode ? 'font-mono text-sm' : '';
    return `
        <div class="question-card bg-gray-50 dark:bg-gray-700/50 rounded-xl p-5 border dark:border-gray-600" style="border-color: rgba(229, 231, 235, 1);" data-question-id="${question.id}">
            <!-- Question Header -->
            <div class="flex items-start justify-between mb-4">
                <div class="flex items-center gap-2">
                    <span class="text-sm font-semibold text-gray-400 dark:text-gray-500">#${orderNum}</span>
                    <span class="px-2 py-1 text-xs font-medium bg-${difficultyLabel.color}-100 dark:bg-${difficultyLabel.color}-900/30 text-${difficultyLabel.color}-600 dark:text-${difficultyLabel.color}-400 rounded-lg">${difficultyLabel.text}</span>
                    ${question.user_edited ? '<span class="px-2 py-1 text-xs font-medium bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 rounded-lg">Thủ công</span>' : '<span class="px-2 py-1 text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-lg">Tự động</span>'}
                </div>
            </div>

            <!-- Question Content -->
            <h4 class="text-gray-900 dark:text-white font-medium mb-4 whitespace-pre-wrap break-words ${stemExtraClass}">${escapeHtml(displayContent)}</h4>

            <!-- Options -->
            <div class="space-y-2">
                ${question.options.map(opt => `
                    <div class="option-item flex items-center gap-3 p-3 rounded-lg ${opt.is_correct ? 'bg-green-50 dark:bg-green-900/20 border-2 border-green-500' : 'bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600'}">
                        <span class="w-8 h-8 flex items-center justify-center rounded-lg ${opt.is_correct ? 'bg-green-500 text-white' : 'bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300'} font-medium text-sm">${opt.id}</span>
                        <span class="flex-1 text-gray-700 dark:text-gray-300 whitespace-pre-wrap break-words">${escapeHtml(formatDisplayText(opt.text))}</span>
                        ${opt.is_correct ? '<svg class="w-5 h-5 text-green-500 flex-shrink-0" fill="currentColor" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>' : ''}
                    </div>
                `).join('')}
            </div>

            <!-- Explanation -->
            ${question.explanation ? `
            <div class="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800">
                <div class="flex items-start gap-2">
                    <svg class="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <p class="text-sm text-blue-700 dark:text-blue-300 whitespace-pre-wrap break-words">${escapeHtml(formatDisplayText(question.explanation))}</p>
                </div>
            </div>
            ` : ''}
        </div>
    `;
}

/**
 * Load and display questions in modal for a specific subject
 */
async function loadModalSubjectQuestions(subjectId) {
    const modal = document.getElementById('questionsModal');
    const modalTitle = document.getElementById('modalTitle');
    const modalLoading = document.getElementById('modalLoading');
    const modalQuestionsList = document.getElementById('modalQuestionsList');
    const modalEmptyState = document.getElementById('modalEmptyState');
    
    if (!modal) return;
    
    // Show modal and loading state
    modal.classList.remove('hidden');
    modalLoading.classList.remove('hidden');
    modalQuestionsList.innerHTML = '';
    modalEmptyState.classList.add('hidden');
    
    try {
        // Fetch questions for this subject
        const url = DASHBOARD_API_ENDPOINTS.getQuestions + `?subject_id=${subjectId}`;
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            throw new Error('Không thể tải câu hỏi');
        }
        
        const data = await response.json();
        
        // Get subject title from the clicked item
        const subjectItem = document.querySelector(`[subject-id="${subjectId}"]`);
        let subjectTitle = 'Câu hỏi';
        if (subjectItem) {
            const titleElement = subjectItem.querySelector('h3');
            if (titleElement) {
                subjectTitle = titleElement.textContent.trim() || 'Câu hỏi';
            }
        }
        
        // Set modal title
        modalTitle.textContent = subjectTitle;
        
        // Hide loading
        modalLoading.classList.add('hidden');
        
        if (data.success && data.questions && data.questions.length > 0) {
            // Display questions
            const difficultyLabels = {
                'easy': { text: 'Easy', color: 'green' },
                'medium': { text: 'Medium', color: 'blue' },
                'hard': { text: 'Hard', color: 'red' }
            };
            
            data.questions.forEach((question, index) => {
                const difficultyKey = (question.difficulty || 'medium').toLowerCase();
                const difficultyLabel = difficultyLabels[difficultyKey] || difficultyLabels['medium'];
                const questionHTML = createQuestionCardHTML(question, index + 1, difficultyLabel);
                modalQuestionsList.insertAdjacentHTML('beforeend', questionHTML);
            });
            
            modalEmptyState.classList.add('hidden');
        } else {
            // No questions
            modalQuestionsList.innerHTML = '';
            modalEmptyState.classList.remove('hidden');
        }
    } catch (error) {
        console.error('Error loading questions for modal:', error);
        modalLoading.classList.add('hidden');
        modalEmptyState.classList.remove('hidden');
        showToast('Không thể tải câu hỏi', 'error');
    }
}

/**
 * Close questions modal
 */
function closeQuestionsModal() {
    const modal = document.getElementById('questionsModal');
    if (modal) {
        modal.classList.add('hidden');
    }
}

// Close modal on ESC key
document.addEventListener('keydown', function(event) {
    if (event.key === 'Escape') {
        const modal = document.getElementById('questionsModal');
        if (modal && !modal.classList.contains('hidden')) {
            closeQuestionsModal();
        }
    }
});

/**
 * Delete Subject
 */
async function deleteSubject(id, title) {
    if (!confirm(`Bạn có chắc muốn xóa môn học "${title}"?\n\nHành động này không thể hoàn tác.`)) {
        return;
    }
    
    try {
        const response = await fetch(`/api/subjects/${id}/delete/`, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            }
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast(data.message, 'success');
            // Reload page to refresh the list
            setTimeout(() => {
                window.location.reload();
            }, 1000);
        } else {
            showToast(data.error || 'Có lỗi xảy ra', 'error');
        }
    } catch (error) {
        console.error('Error deleting subject:', error);
        showToast('Không thể xóa môn học', 'error');
    }
}
