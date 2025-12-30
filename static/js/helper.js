/**
 * Shared Helper Functions
 * Common utilities used across controlgen.js and dashboard.js
 */

// ============== CSRF TOKEN ==============

/**
 * Get CSRF token from cookies for Django
 * @returns {string|null} CSRF token value
 */
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

// ============== TEXT UTILITIES ==============

/**
 * Escape HTML to prevent XSS attacks
 * @param {string} text - Text to escape
 * @returns {string} Escaped HTML string
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

/**
 * Normalize text for display: convert <br> tags to newline
 * @param {string} text - Text containing HTML
 * @returns {string} Text with newlines
 */
function formatDisplayText(text) {
    if (!text) return '';
    return String(text).replace(/<br\s*\/?>/gi, '\n');
}

// ============== TOAST NOTIFICATIONS ==============

/**
 * Show toast notification with animation
 * @param {string} message - Message to display
 * @param {string} type - Type: 'success', 'error', 'warning', 'info'
 */
function showToast(message, type = 'info') {
    // Remove existing toasts with animation
    const existingToasts = document.querySelectorAll('.toast-notification');
    existingToasts.forEach(t => {
        t.style.opacity = '0';
        t.style.transform = 'translateX(100%)';
        setTimeout(() => t.remove(), 200);
    });

    // Create toast element
    const toast = document.createElement('div');
    toast.className = 'toast-notification fixed top-20 right-4 z-50 flex items-center gap-3 px-4 py-3 rounded-xl shadow-lg transition-all duration-300';

    // Set color based on type
    const colors = {
        success: 'bg-green-500 text-white shadow-green-500/30',
        error: 'bg-red-500 text-white shadow-red-500/30',
        warning: 'bg-yellow-500 text-white shadow-yellow-500/30',
        info: 'bg-blue-500 text-white shadow-blue-500/30'
    };
    toast.className += ' ' + (colors[type] || colors.info);

    // Set icon
    const icons = {
        success: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12l2 2 4-4m6 2a9 9 0 11-18 0 9 9 0 0118 0z"/>',
        error: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 8v4m0 4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>',
        warning: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M12 9v2m0 4h.01m-6.938 4h13.856c1.54 0 2.502-1.667 1.732-3L13.732 4c-.77-1.333-2.694-1.333-3.464 0L3.34 16c-.77 1.333.192 3 1.732 3z"/>',
        info: '<path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>'
    };

    // Initial state for animation
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

    // Trigger entrance animation
    requestAnimationFrame(() => {
        toast.style.opacity = '1';
        toast.style.transform = 'translateX(0)';
    });

    // Auto remove after 4 seconds
    setTimeout(() => closeToast(toast), 4000);
}

/**
 * Close toast with animation
 * @param {HTMLElement} toast - Toast element to close
 */
function closeToast(toast) {
    if (!toast || !toast.parentElement) return;

    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
}

// ============== DIFFICULTY LABELS ==============

/**
 * Get difficulty label configuration
 * @param {string} difficulty - Difficulty level: 'easy', 'medium', 'hard'
 * @returns {Object} Label config with text and color
 */
function getDifficultyLabel(difficulty) {
    const labels = {
        'easy': { text: 'Easy', color: 'green' },
        'medium': { text: 'Medium', color: 'blue' },
        'hard': { text: 'Hard', color: 'red' }
    };
    const key = (difficulty || 'medium').toLowerCase();
    return labels[key] || labels['medium'];
}

// ============== QUESTION CARD HTML ==============

/**
 * Create Question Card HTML for display (read-only version)
 * Used in dashboard modal
 * @param {Object} question - Question data
 * @param {number} orderNum - Question order number
 * @param {Object} difficultyLabel - Difficulty label config
 * @returns {string} HTML string
 */
function createReadOnlyQuestionCardHTML(question, orderNum, difficultyLabel) {
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

// ============== TIME FORMATTING ==============

/**
 * Format time ago in Vietnamese
 * @param {string} isoString - ISO date string
 * @returns {string} Formatted time ago
 */
function formatTimeAgo(isoString) {
    const date = new Date(isoString);
    const now = new Date();
    const diffMs = now - date;
    const diffMins = Math.floor(diffMs / 60000);
    const diffHours = Math.floor(diffMs / 3600000);
    const diffDays = Math.floor(diffMs / 86400000);

    if (diffMins < 1) return 'vừa xong';
    if (diffMins < 60) return `${diffMins} phút trước`;
    if (diffHours < 24) return `${diffHours} giờ trước`;
    return `${diffDays} ngày trước`;
}

/**
 * Format difficulty in Vietnamese
 * @param {string} difficulty - Difficulty level
 * @returns {string} Formatted difficulty
 */
function formatDifficulty(difficulty) {
    const map = { 'easy': 'Dễ', 'medium': 'Trung bình', 'hard': 'Khó' };
    return map[difficulty] || difficulty;
}
