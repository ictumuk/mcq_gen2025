/**
 * MCQ Generator Controller
 * Handles all interactive functionality for the MCQ Generator page
 */

// API Configuration
const API_ENDPOINTS = {
    createQuestion: '/api/questions/create/',
    getQuestions: '/api/questions/',
    updateQuestion: (id) => `/api/questions/${id}/update/`,
    deleteQuestion: (id) => `/api/questions/${id}/delete/`,
    deleteSubject: (id) => `/api/subjects/${id}/delete/`,
    clearAllQuestions: '/api/questions/clear-all/',
    getSubjectsList: '/api/subjects/list/',
    getSubjectsHistory: '/api/subjects/history/'
};

// Cached uploaded file state (memory only per page session)
let cachedSourceFile = null; // { id, name, size }

// Questions pagination state
let currentSubjectId = null;
let currentSubjectName = null; // Store current subject name for export
let currentPage = 1;
let questionsPerPage = 5; // Maximum 5 questions per page
let questionsToShow = 2; // Initial show 2 questions, scroll to show more
let allQuestions = []; // Store all questions for current subject

// ============== HELPER FUNCTIONS ==============

/**
 * Create checkmark SVG element
 */
function createCheckmarkSVG() {
    const svg = document.createElement('svg');
    svg.className = 'w-5 h-5 text-green-500 flex-shrink-0 animate-success-pop';
    svg.setAttribute('fill', 'currentColor');
    svg.setAttribute('viewBox', '0 0 24 24');
    svg.innerHTML = '<path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/>';
    return svg;
}

/**
 * Style option item as correct or incorrect
 * @param {Element} optItem - The option item element
 * @param {boolean} isCorrect - Whether this option is the correct answer
 */
function setOptionStyle(optItem, isCorrect) {
    const labelSpan = optItem.querySelector('.answer-btn, .w-8.h-8');
    const existingCheck = optItem.querySelector('svg.text-green-500');
    
    if (isCorrect) {
        // Correct answer styling
        optItem.classList.remove('bg-white', 'dark:bg-gray-700', 'border', 'border-gray-200', 'dark:border-gray-600', 'hover:border-blue-400');
        optItem.classList.add('bg-green-50', 'dark:bg-green-900/20', 'border-2', 'border-green-500');
        
        if (labelSpan) {
            labelSpan.classList.remove('bg-gray-200', 'dark:bg-gray-600', 'text-gray-600', 'dark:text-gray-300');
            labelSpan.classList.add('bg-green-500', 'text-white');
        }
        
        // Add checkmark if not exists
        if (!existingCheck) {
            optItem.appendChild(createCheckmarkSVG());
        }
    } else {
        // Incorrect answer styling
        optItem.classList.remove('bg-green-50', 'dark:bg-green-900/20', 'border-2', 'border-green-500');
        optItem.classList.add('bg-white', 'dark:bg-gray-700', 'border', 'border-gray-200', 'dark:border-gray-600', 'hover:border-blue-400');
        
        if (labelSpan) {
            labelSpan.classList.remove('bg-green-500', 'text-white');
            labelSpan.classList.add('bg-gray-200', 'dark:bg-gray-600', 'text-gray-600', 'dark:text-gray-300');
        }
        
        // Remove checkmark if exists
        if (existingCheck) {
            existingCheck.remove();
        }
    }
}

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

document.addEventListener('DOMContentLoaded', function() {
    initTabs();
    initCharacterCount();
    initQuantitySlider();
    initFileUpload();
    initGenerateButton();
    initDifficultyButtons();
    initQuestionTypeCheckboxes();
    initModalAnimations();
    initSubjectSelect();
    initModalSubjectSelect();
    attachHistoryItemListeners();
    
    // Load existing questions from backend
    loadQuestionsFromBackend();
});

/**
 * Initialize Modal Animations
 */
function initModalAnimations() {
    const modal = document.getElementById('addQuestionModal');
    if (!modal) return;
    
    // Add animation classes
    const backdrop = modal.querySelector('.modal-backdrop');
    const content = modal.querySelector('.modal-content');
    
    if (backdrop) {
        backdrop.style.transition = 'opacity 0.3s ease';
    }
    if (content) {
        content.style.transition = 'all 0.3s cubic-bezier(0.4, 0, 0.2, 1)';
    }
}

/**
 * Load Questions from Backend
 */
async function loadQuestionsFromBackend(subjectId = null) {
    try {
        let url = API_ENDPOINTS.getQuestions;
        if (subjectId) {
            url += `?subject_id=${subjectId}`;
        }
        
        const response = await fetch(url, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (!response.ok) {
            // User might not be logged in or no questions yet
            console.log('Could not load questions from backend');
            return;
        }
        
        const data = await response.json();
        
        if (data.success && data.questions && data.questions.length > 0) {
            // Store all questions for pagination
            allQuestions = data.questions;
            currentSubjectId = subjectId;
            currentPage = 1;
            
            // Try to get subject name from various sources
            if (!currentSubjectName) {
                if (subjectId) {
                    // First, try to get from history items in DOM
                    const historyItem = document.querySelector(`[data-subject-id="${subjectId}"]`);
                    if (historyItem) {
                        const titleElement = historyItem.querySelector('p.text-sm.font-medium');
                        if (titleElement) {
                            currentSubjectName = titleElement.textContent.trim();
                        }
                    }
                    
                    // If still not found, try to fetch from history API
                    if (!currentSubjectName) {
                        try {
                            const historyResponse = await fetch(API_ENDPOINTS.getSubjectsHistory, {
                                method: 'GET',
                                headers: {
                                    'Content-Type': 'application/json',
                                }
                            });
                            
                            if (historyResponse.ok) {
                                const historyData = await historyResponse.json();
                                if (historyData.success && historyData.subjects) {
                                    const subject = historyData.subjects.find(s => s.id === subjectId);
                                    if (subject) {
                                        // Use title if available, otherwise use subject field
                                        currentSubjectName = subject.title || subject.subject || null;
                                    }
                                }
                            }
                        } catch (err) {
                            console.log('Could not fetch subject from history:', err);
                        }
                    }
                } else {
                    // No subject_id - try to get from latest subject in history
                    try {
                        const historyResponse = await fetch(API_ENDPOINTS.getSubjectsHistory, {
                            method: 'GET',
                            headers: {
                                'Content-Type': 'application/json',
                            }
                        });
                        
                        if (historyResponse.ok) {
                            const historyData = await historyResponse.json();
                            if (historyData.success && historyData.subjects && historyData.subjects.length > 0) {
                                // Get the latest subject (first in the list)
                                const latestSubject = historyData.subjects[0];
                                currentSubjectName = latestSubject.title || latestSubject.subject || null;
                                currentSubjectId = latestSubject.id;
                            }
                        }
                    } catch (err) {
                        console.log('Could not fetch latest subject from history:', err);
                    }
                }
            }
            
            // If still not found, try to get from subject select/input
            if (!currentSubjectName) {
                const subjectSelect = document.getElementById('subjectSelect');
                const subjectInput = document.getElementById('subjectInput');
                if (subjectSelect && subjectSelect.value && subjectSelect.value !== '__new__') {
                    const selectedOption = subjectSelect.options[subjectSelect.selectedIndex];
                    if (selectedOption.hasAttribute('data-subject-name')) {
                        currentSubjectName = selectedOption.getAttribute('data-subject-name');
                    } else {
                        currentSubjectName = subjectSelect.value.trim();
                    }
                } else if (subjectInput && !subjectInput.classList.contains('hidden')) {
                    currentSubjectName = subjectInput.value.trim();
                }
            }
            
            // Display first page
            displayQuestionsPage(1);
            updateQuestionCount();
        } else {
            // No questions
            const emptyState = document.getElementById('emptyState');
            const questionsContainer = document.getElementById('questionsContainer');
            if (emptyState) emptyState.classList.remove('hidden');
            if (questionsContainer) {
                questionsContainer.classList.add('hidden');
                questionsContainer.innerHTML = '';
            }
            allQuestions = [];
            currentSubjectName = null;
            updateQuestionCount();
        }
    } catch (error) {
        console.log('Error loading questions:', error);
    }
}

/**
 * Display questions for a specific page with scroll-based loading
 */
function displayQuestionsPage(page) {
    const emptyState = document.getElementById('emptyState');
    const questionsContainer = document.getElementById('questionsContainer');
    
    if (!questionsContainer) return;
    
    if (allQuestions.length === 0) {
        if (emptyState) emptyState.classList.remove('hidden');
        questionsContainer.classList.add('hidden');
        questionsContainer.innerHTML = '';
        updatePaginationControls();
        return;
    }
    
    if (emptyState) emptyState.classList.add('hidden');
    questionsContainer.classList.remove('hidden');
    
    // Calculate pagination
    const totalPages = Math.ceil(allQuestions.length / questionsPerPage);
    const startIndex = (page - 1) * questionsPerPage;
    const questionsToDisplay = Math.min(questionsPerPage, allQuestions.length - startIndex);
    const pageQuestions = allQuestions.slice(startIndex, startIndex + questionsToDisplay);
    
    // Remove any existing scroll handler before clearing
    if (questionsContainer._scrollHandler) {
        questionsContainer.removeEventListener('scroll', questionsContainer._scrollHandler);
        delete questionsContainer._scrollHandler;
    }
    
    // Clear and render all questions for this page
    questionsContainer.innerHTML = '';
    
    // Display all questions for the current page
    pageQuestions.forEach((q, index) => {
        // Calculate correct question number (1-based, global index)
        const questionNumber = startIndex + index + 1;
        addQuestionToUIFromData(q, questionNumber);
    });
    
    // Add pagination controls
    updatePaginationControls(totalPages, page, allQuestions.length);
}

/**
 * Update pagination controls
 */
function updatePaginationControls(totalPages = 0, currentPageNum = 1, totalQuestions = 0) {
    const questionsContainer = document.getElementById('questionsContainer');
    if (!questionsContainer) return;
    
    // Remove existing pagination
    const existingPagination = questionsContainer.querySelector('.questions-pagination');
    if (existingPagination) {
        existingPagination.remove();
    }
    
    if (totalPages <= 1 && totalQuestions <= questionsPerPage) return; // No pagination needed
    
    // Create pagination controls
    const paginationHTML = `
        <div class="questions-pagination mt-4 pt-4 border-t border-gray-200 dark:border-gray-700 flex items-center justify-between">
            <div class="text-sm text-gray-600 dark:text-gray-400">
                ${totalPages > 1 ? `Trang ${currentPageNum} / ${totalPages}` : ''} (${totalQuestions} câu hỏi)
            </div>
            ${totalPages > 1 ? `
            <div class="flex items-center gap-2">
                <button onclick="goToQuestionsPage(${currentPageNum - 1})" 
                        ${currentPageNum === 1 ? 'disabled' : ''}
                        class="px-3 py-1.5 text-sm font-medium rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
                    ← Trước
                </button>
                <button onclick="goToQuestionsPage(${currentPageNum + 1})" 
                        ${currentPageNum === totalPages ? 'disabled' : ''}
                        class="px-3 py-1.5 text-sm font-medium rounded-lg border border-gray-300 dark:border-gray-600 text-gray-700 dark:text-gray-300 hover:bg-gray-50 dark:hover:bg-gray-700 disabled:opacity-50 disabled:cursor-not-allowed transition-colors">
                    Sau →
                </button>
            </div>
            ` : ''}
        </div>
    `;
    
    questionsContainer.insertAdjacentHTML('beforeend', paginationHTML);
}

/**
 * Go to specific questions page
 */
function goToQuestionsPage(page) {
    const totalPages = Math.ceil(allQuestions.length / questionsPerPage);
    if (page < 1 || page > totalPages) return;
    
    currentPage = page;
    displayQuestionsPage(page);
    
    // Scroll to top of questions container
    const questionsContainer = document.getElementById('questionsContainer');
    if (questionsContainer) {
        questionsContainer.scrollIntoView({ behavior: 'smooth', block: 'start' });
    }
}

/**
 * Load questions for a specific subject
 */
async function loadSubjectQuestions(subjectId) {
    // Highlight selected history item
    document.querySelectorAll('.history-item').forEach(item => {
        item.classList.remove('bg-blue-50', 'dark:bg-blue-900/20', 'border-blue-500');
        item.classList.add('bg-gray-50', 'dark:bg-gray-700');
    });
    
    const selectedItem = document.querySelector(`[data-subject-id="${subjectId}"]`);
    if (selectedItem) {
        selectedItem.classList.remove('bg-gray-50', 'dark:bg-gray-700');
        selectedItem.classList.add('bg-blue-50', 'dark:bg-blue-900/20', 'border', 'border-blue-500');
        
        // Extract subject name from history item
        const titleElement = selectedItem.querySelector('p.text-sm.font-medium');
        if (titleElement) {
            currentSubjectName = titleElement.textContent.trim();
        }
    }
    
    // Load questions for this subject
    await loadQuestionsFromBackend(subjectId);
    
    // Scroll to questions section after loading
    setTimeout(() => {
        const questionsList = document.getElementById('questionsList');
        const resultsSection = document.getElementById('resultsSection');
        const targetElement = questionsList || resultsSection;
        
        if (targetElement) {
            targetElement.scrollIntoView({ 
                behavior: 'smooth', 
                block: 'start',
                inline: 'nearest'
            });
        }
    }, 100); // Small delay to ensure DOM is updated
}
/**
 * Refresh history panel with latest subjects
 */
async function refreshHistoryPanel() {
    try {
        const response = await fetch(API_ENDPOINTS.getSubjectsHistory, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.subjects) {
                updateHistoryPanelUI(data.subjects);
            }
        }
    } catch (error) {
        console.error('Error refreshing history panel:', error);
        // Fallback: reload page
        setTimeout(() => {
            window.location.reload();
        }, 500);
    }
}

/**
 * Update history panel UI with new subjects data
 */
function updateHistoryPanelUI(subjects) {
    const historyContainer = document.querySelector('.bg-white.dark\\:bg-gray-800.rounded-2xl.shadow-xl .p-4.space-y-3');
    if (!historyContainer) return;
    
    if (subjects.length === 0) {
        historyContainer.innerHTML = `
            <div class="px-6 py-16 text-center">
                <p class="text-sm text-gray-500">Chưa có lịch sử gần đây</p>
            </div>
        `;
        return;
    }
    
    // Format time ago
    const formatTimeAgo = (isoString) => {
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
    };
    
    // Format difficulty
    const formatDifficulty = (diff) => {
        const map = { 'easy': 'Dễ', 'medium': 'Trung bình', 'hard': 'Khó' };
        return map[diff] || diff;
    };
    
    // Generate history items HTML
    const historyHTML = subjects.map(subj => `
        <div class="history-item flex items-center gap-3 p-3 bg-gray-50 dark:bg-gray-700 rounded-lg hover:bg-gray-100 dark:hover:bg-gray-600 cursor-pointer transition-colors" 
             data-subject-id="${subj.id}" 
             onclick="loadSubjectQuestions('${subj.id}')">
            <div class="w-10 h-10 bg-blue-100 dark:bg-blue-900/30 rounded-lg flex items-center justify-center flex-shrink-0">
                <svg class="w-5 h-5 text-blue-600" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M9 12h6m-6 4h6m2 5H7a2 2 0 01-2-2V5a2 2 0 012-2h5.586a1 1 0 01.707.293l5.414 5.414a1 1 0 01.293.707V19a2 2 0 01-2 2z"/>
                </svg>
            </div>
            <div class="flex-1 min-w-0">
                <p class="text-sm font-medium text-gray-900 dark:text-white truncate">${escapeHtml(subj.title)}</p>
                <div class="flex items-center gap-3 mt-1 text-sm text-gray-500 dark:text-gray-400">
                    <span class="flex items-center gap-1">
                        <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M8.228 9c.549-1.165 2.03-2 3.772-2 2.21 0 4 1.343 4 3 0 1.4-1.278 2.575-3.006 2.907-.542.104-.994.54-.994 1.093m0 3h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                        </svg>
                        ${subj.question_count} câu hỏi
                    </span>
                    <span>•</span>
                    <span>${formatDifficulty(subj.difficulty)}</span>
                    <span>•</span>
                    <span>${formatTimeAgo(subj.updated_at || subj.created_at)}</span>
                </div>
            </div>
        </div>
    `).join('');
    
    historyContainer.innerHTML = historyHTML;
    
    // Re-attach event listeners
    attachHistoryItemListeners();
}

/**
 * Attach event listeners to history items
 */
function attachHistoryItemListeners() {
    document.querySelectorAll('.history-item').forEach(item => {
        const subjectId = item.getAttribute('data-subject-id');
        if (subjectId) {
            item.addEventListener('click', () => {
                loadSubjectQuestions(subjectId);
            });
        }
    });
}

/**
 * Add Question to UI from backend data
 */
function addQuestionToUIFromData(question, orderNum) {
    const container = document.getElementById('questionsContainer');
    if (!container) return;
    
    const difficultyLabels = {
        'easy': { text: 'Easy', color: 'green' },
        'medium': { text: 'Medium', color: 'blue' },
        'hard': { text: 'Hard', color: 'red' }
    };
    const difficultyKey = (question.difficulty || 'medium').toLowerCase();
    const difficultyLabel = difficultyLabels[difficultyKey] || difficultyLabels['medium'];
    
    const questionHTML = createQuestionCardHTML(question, orderNum, difficultyLabel);
    container.insertAdjacentHTML('beforeend', questionHTML);
    
    // Save original data immediately after rendering for cancel functionality
    const newCard = container.lastElementChild;
    if (newCard) {
        // Store the original question object directly
        originalQuestionData.set(question.id, {
            stem: question.stem || question.content || '',
            explanation: question.explanation || question.explanation + 'Không có giải thích',
            options: (question.options || []).map(opt => ({
                id: opt.id,
                text: opt.text || '',
                is_correct: opt.is_correct || false
            }))
        });
    }
}

// Toast notification - moved to bottom of file with enhanced version

/**
 * Dark Mode Toggle
 */
function initDarkMode() {
    const darkModeToggle = document.getElementById('darkModeToggle');
    const html = document.documentElement;
    
    // Check for saved dark mode preference
    if (localStorage.getItem('darkMode') === 'true') {
        html.classList.add('dark');
    }
    
    if (darkModeToggle) {
        darkModeToggle.addEventListener('click', () => {
            html.classList.toggle('dark');
            localStorage.setItem('darkMode', html.classList.contains('dark'));
        });
    }
}

/**
 * Update User Credits display on UI
 */
function updateUserCredits(credits) {
    if (credits === undefined || credits === null) return;
    
    // Update navbar credits
    const navCredits = document.getElementById('navCredits');
    if (navCredits) {
        navCredits.textContent = `${credits} credits`;
    }
    
    // Update page credits (in generate_mcq.html)
    const pageCredits = document.getElementById('pageCredits');
    if (pageCredits) {
        // Use innerHTML to preserve the <strong> tag if needed, 
        // but here we just update the numeric part if we want to be safe
        pageCredits.innerHTML = `Bạn có <strong>${credits}</strong> credits`;
    }
    
    // Update dashboard credits
    const dashboardCredits = document.getElementById('dashboardCredits');
    if (dashboardCredits) {
        dashboardCredits.textContent = credits;
    }
}

/**
 * Tab Switching
 */
function initTabs() {
    const inputTabs = document.querySelectorAll('.input-tab');
    const tabContents = {
        text: document.getElementById('textTab'),
        file: document.getElementById('fileTab'),
        url: document.getElementById('urlTab')
    };

    inputTabs.forEach(tab => {
        tab.addEventListener('click', () => {
            // Remove active class from all tabs
            inputTabs.forEach(t => {
                t.classList.remove('tab-active');
                t.classList.add('text-gray-600', 'dark:text-gray-300');
            });
            
            // Add active class to clicked tab
            tab.classList.add('tab-active');
            tab.classList.remove('text-gray-600', 'dark:text-gray-300');
            
            // Hide all tab contents
            Object.values(tabContents).forEach(content => {
                if (content) content.classList.add('hidden');
            });
            
            // Show selected tab content
            const tabName = tab.dataset.tab;
            if (tabContents[tabName]) {
                tabContents[tabName].classList.remove('hidden');
            }
        });
    });
}

/**
 * Character Count
 */
function initCharacterCount() {
    const textInput = document.getElementById('textInput');
    const charCount = document.getElementById('charCount');
    
    if (textInput && charCount) {
        textInput.addEventListener('input', () => {
            charCount.textContent = `${textInput.value.length} ký tự`;
        });
    }
}

/**
 * Quantity Slider
 */
function initQuantitySlider() {
    const quantitySlider = document.getElementById('quantitySlider');
    const quantityValue = document.getElementById('quantityValue');
    
    if (quantitySlider && quantityValue) {
        // Set initial progress
        updateSliderProgress(quantitySlider);
        
        quantitySlider.addEventListener('input', (e) => {
            const value = e.target.value;
            quantityValue.textContent = value;
            updateSliderProgress(e.target);
        });
    }
}

function updateSliderProgress(slider) {
    const value = slider.value;
    const min = slider.min || 1;
    const max = slider.max || 50;
    const progress = ((value - min) / (max - min)) * 100;
    slider.style.setProperty('--progress', `${progress}%`);
    const quantityValue = document.getElementById('quantityValue');
    if (quantityValue) quantityValue.textContent = value;
}

/**
 * Load subjects list from API
 */
async function loadSubjectsList() {
    try {
        const response = await fetch(API_ENDPOINTS.getSubjectsList, {
            method: 'GET',
            headers: {
                'Content-Type': 'application/json',
            }
        });
        
        if (response.ok) {
            const data = await response.json();
            if (data.success && data.subjects && data.subjects.length > 0) {
                return data.subjects;
            }
        }
    } catch (error) {
        console.error('Error loading subjects list:', error);
    }
    return [];
}

/**
 * Populate subject select with subjects list
 */
function populateSubjectSelect(selectElement, subjects) {
    if (!selectElement) return;
    
    const newOption = selectElement.querySelector('option[value="__new__"]');
    // Remove existing subject options (keep default and new option)
    const existingOptions = selectElement.querySelectorAll('option:not([value=""]):not([value="__new__"])');
    existingOptions.forEach(opt => opt.remove());
    
    // Add subjects - subjects can be array of strings (old format) or array of objects (new format)
    subjects.forEach(subject => {
        const option = document.createElement('option');
        // Support both old format (string) and new format (object with id and name)
        if (typeof subject === 'string') {
            option.value = subject;
            option.textContent = subject;
        } else {
            // New format: {id, name}
            option.value = subject.id;
            option.setAttribute('data-subject-name', subject.name);
            option.textContent = subject.name;
        }
        if (newOption) {
            selectElement.insertBefore(option, newOption);
        } else {
            selectElement.appendChild(option);
        }
    });
}

/**
 * Initialize Subject Select and Input for main form
 */
async function initSubjectSelect() {
    const subjectSelect = document.getElementById('subjectSelect');
    const subjectInput = document.getElementById('subjectInput');
    
    if (!subjectSelect || !subjectInput) return;
    
    // Load and populate subjects
    const subjects = await loadSubjectsList();
    populateSubjectSelect(subjectSelect, subjects);
    
    // Handle select change
    subjectSelect.addEventListener('change', function() {
        if (this.value === '__new__') {
            // Show input for new subject
            subjectInput.classList.remove('hidden');
            subjectInput.value = '';
            subjectInput.focus();
        } else if (this.value) {
            // Hide input, use selected value
            subjectInput.classList.add('hidden');
            // Get subject name from option's data attribute or value
            const selectedOption = this.options[this.selectedIndex];
            if (selectedOption.hasAttribute('data-subject-name')) {
                subjectInput.value = selectedOption.getAttribute('data-subject-name');
            } else {
                subjectInput.value = this.value;
            }
        } else {
            // No selection
            subjectInput.classList.add('hidden');
            subjectInput.value = '';
        }
    });
    
    // Handle input change when creating new subject
    subjectInput.addEventListener('input', function() {
        if (!subjectInput.classList.contains('hidden')) {
            // Ensure select is set to "Tạo môn học mới"
            if (subjectSelect.value !== '__new__') {
                subjectSelect.value = '__new__';
            }
        }
    });
}

/**
 * Initialize Subject Select and Input for modal
 */
async function initModalSubjectSelect() {
    const subjectSelect = document.getElementById('newQuestionSubjectSelect');
    const subjectInput = document.getElementById('newQuestionSubjectInput');
    
    if (!subjectSelect || !subjectInput) return;
    
    // Load and populate subjects
    const subjects = await loadSubjectsList();
    populateSubjectSelect(subjectSelect, subjects);
    
    // Handle select change
    subjectSelect.addEventListener('change', function() {
        if (this.value === '__new__') {
            // Show input for new subject
            subjectInput.classList.remove('hidden');
            subjectInput.value = '';
            subjectInput.focus();
        } else if (this.value) {
            // Hide input, use selected value
            subjectInput.classList.add('hidden');
            // Get subject name from option's data attribute or value
            const selectedOption = this.options[this.selectedIndex];
            if (selectedOption.hasAttribute('data-subject-name')) {
                subjectInput.value = selectedOption.getAttribute('data-subject-name');
            } else {
                subjectInput.value = this.value;
            }
        } else {
            // No selection
            subjectInput.classList.add('hidden');
            subjectInput.value = '';
        }
    });
    
    // Handle input change when creating new subject
    subjectInput.addEventListener('input', function() {
        if (!subjectInput.classList.contains('hidden')) {
            // Ensure select is set to "Tạo môn học mới"
            if (subjectSelect.value !== '__new__') {
                subjectSelect.value = '__new__';
            }
        }
    });
}

/**
 * Generate payload for MCQ generation
 */
function getGenerationPayload() {
    const textInput = document.getElementById('textInput');
    const subjectSelect = document.getElementById('subjectSelect');
    const subjectInput = document.getElementById('subjectInput');
    const topicInput = document.getElementById('topicInput');
    const keyPointInput = document.getElementById('keyPointInput');
    const quantitySlider = document.getElementById('quantitySlider');
    const difficultyValue = document.getElementById('difficultyValue');

    const text = textInput ? textInput.value.trim() : '';
    
    // Get subject and subject_id from select or input
    let subject = '';
    let subject_id = null;
    
    if (subjectSelect && subjectSelect.value === '__new__' && subjectInput) {
        // New subject from input
        subject = subjectInput.value.trim();
        subject_id = null;
    } else if (subjectSelect && subjectSelect.value && subjectSelect.value !== '__new__') {
        // Existing subject from select
        const selectedOption = subjectSelect.options[subjectSelect.selectedIndex];
        // Check if it's new format (has data-subject-name) or old format (value is name)
        if (selectedOption.hasAttribute('data-subject-name')) {
            subject_id = subjectSelect.value.trim();
            subject = selectedOption.getAttribute('data-subject-name');
        } else {
            // Old format: value is the subject name
            subject = subjectSelect.value.trim();
            subject_id = null;
        }
    } else if (subjectInput && !subjectInput.classList.contains('hidden')) {
        // Fallback to input if visible
        subject = subjectInput.value.trim();
        subject_id = null;
    }
    
    const topic = topicInput ? topicInput.value.trim() : '';
    const key_point = keyPointInput ? keyPointInput.value.trim() : '';
    const number_contexts = quantitySlider ? parseInt(quantitySlider.value, 10) || 3 : 3;
    const level = difficultyValue ? difficultyValue.value : 'medium';

    const payload = {
        text,
        subject,
        topic,
        key_point,
        number_contexts,
        level,
        model: 'gemini-2.5-flash',
        max_iterations: 3,
        max_workers: 1,
        delay_seconds: 5.0
    };
    
    // Add subject_id if available
    if (subject_id) {
        payload.subject_id = subject_id;
    }
    
    return payload;
}

/**
 * Cached upload helpers
 */
function setCachedUpload(source_file_id, name, size) {
    cachedSourceFile = { id: source_file_id, name, size };
    updateUploadedBadge();
}

function clearCachedUpload() {
    cachedSourceFile = null;
    const fileInput = document.getElementById('fileInput');
    if (fileInput) fileInput.value = '';
    updateUploadedBadge();
}

function updateUploadedBadge() {
    const badge = document.getElementById('uploadedBadge');
    const label = document.getElementById('uploadedFileLabel');
    if (!badge || !label) return;
    // Chỉ hiển thị khi đã upload thành công và có source_file_id trong cache
    const hasUploaded = cachedSourceFile && cachedSourceFile.id;

    if (hasUploaded) {
        const name = cachedSourceFile.name ? `Đã tải file: ${cachedSourceFile.name}` : 'Đã tải file';
        label.textContent = name;
        badge.style.display = 'inline-flex';
        badge.classList.remove('hidden');
    } else {
        label.textContent = 'Đã tải lên';
        badge.style.display = 'none';
        badge.classList.add('hidden');
    }
}

/**
 * Upload source file to backend, return {source_file_id}
 */
async function uploadSourceFile(file) {
    const formData = new FormData();
    formData.append('file', file);
    const response = await fetch('/api/source/upload/', {
        method: 'POST',
        headers: {
            'X-CSRFToken': getCsrfToken()
        },
        body: formData
    });
    const data = await response.json();
    if (!response.ok || !data.success) {
        throw new Error(data.error || 'Upload file thất bại');
    }
    return data;
}

/**
 * File Upload
 */
function initFileUpload() {
    const uploadZone = document.getElementById('uploadZone');
    const fileInput = document.getElementById('fileInput');
    const filePreview = document.getElementById('filePreview');
    const fileName = document.getElementById('fileName');
    const fileSize = document.getElementById('fileSize');
    const removeFile = document.getElementById('removeFile');
    const uploadProgress = document.getElementById('uploadProgress');
    const progressBar = document.getElementById('progressBar');
    const progressPercent = document.getElementById('progressPercent');
    const clearBadgeBtn = document.getElementById('clearUploadedBadge');

    if (!uploadZone || !fileInput) return;

    // Reset cached upload on init (no persistence across reload)
    cachedSourceFile = null;
    const badge = document.getElementById('uploadedBadge');
    if (badge) {
        badge.style.display = 'none';
        badge.classList.add('hidden');
    }
    updateUploadedBadge();

    // Click to upload
    uploadZone.addEventListener('click', () => fileInput.click());
    
    // Drag and drop handlers
    uploadZone.addEventListener('dragover', (e) => {
        e.preventDefault();
        uploadZone.classList.add('dragover');
    });
    
    uploadZone.addEventListener('dragleave', () => {
        uploadZone.classList.remove('dragover');
    });
    
    uploadZone.addEventListener('drop', (e) => {
        e.preventDefault();
        uploadZone.classList.remove('dragover');
        const files = e.dataTransfer.files;
        if (files.length) handleFile(files[0]);
    });
    
    // File input change
    fileInput.addEventListener('change', (e) => {
        if (e.target.files.length) handleFile(e.target.files[0]);
    });
    
    let uploadInProgress = false;

    // Handle file selection
    async function handleFile(file) {
        if (uploadInProgress) return;
        // Validate file size (max 10MB)
        if (file.size > 10 * 1024 * 1024) {
            alert('File quá lớn! Vui lòng chọn file nhỏ hơn 10MB.');
            return;
        }
        
        // Validate file type
        const allowedTypes = ['.pdf', '.docx', '.pptx', '.txt'];
        const fileExt = '.' + file.name.split('.').pop().toLowerCase();
        if (!allowedTypes.includes(fileExt)) {
            alert('Định dạng file không được hỗ trợ! Vui lòng chọn file PDF, DOCX, PPTX hoặc TXT.');
            return;
        }
        
        if (fileName) fileName.textContent = file.name;
        if (fileSize) fileSize.textContent = formatFileSize(file.size);
        
        uploadZone.classList.add('hidden');
        if (filePreview) filePreview.classList.remove('hidden');
        updateUploadedBadge(); // show badge when file is selected

        // Upload file immediately to server
        uploadInProgress = true;
        if (uploadProgress) {
            uploadProgress.classList.remove('hidden');
            progressBar.style.width = '10%';
            progressPercent.textContent = '10%';
        }

        try {
            const uploadResult = await uploadSourceFile(file);
            if (uploadProgress) {
                progressBar.style.width = '100%';
                progressPercent.textContent = '100%';
            }
            setCachedUpload(uploadResult.source_file_id, file.name, file.size);
            showToast('Tải file thành công', 'success');
        } catch (err) {
            showToast(err.message || 'Không thể tải file', 'error');
            clearCachedUpload();
            fileInput.value = '';
            uploadZone.classList.remove('hidden');
            if (filePreview) filePreview.classList.add('hidden');
        } finally {
            uploadInProgress = false;
            if (uploadProgress) {
                setTimeout(() => uploadProgress.classList.add('hidden'), 400);
            }
            updateUploadedBadge();
        }
    }
    
    // Remove file
    if (removeFile) {
        removeFile.addEventListener('click', () => {
            fileInput.value = '';
            uploadZone.classList.remove('hidden');
            if (filePreview) filePreview.classList.add('hidden');
        });
    }

    if (clearBadgeBtn) {
        clearBadgeBtn.addEventListener('click', () => {
            clearCachedUpload();
            showToast('Đã xóa file đã tải lên khỏi bộ nhớ tạm', 'info');
        });
    }
}

/**
 * Format file size
 */
function formatFileSize(bytes) {
    if (bytes === 0) return '0 Bytes';
    const k = 1024;
    const sizes = ['Bytes', 'KB', 'MB', 'GB'];
    const i = Math.floor(Math.log(bytes) / Math.log(k));
    return parseFloat((bytes / Math.pow(k, i)).toFixed(2)) + ' ' + sizes[i];
}

/**
 * Generate Button
 */
function initGenerateButton() {
    const generateBtn = document.getElementById('generateBtn');
    const loadingState = document.getElementById('loadingState');
    const emptyState = document.getElementById('emptyState');
    const questionsContainer = document.getElementById('questionsContainer');
    const questionCount = document.getElementById('questionCount');

    if (!generateBtn) return;

    generateBtn.addEventListener('click', async () => {
        // Validate input
        const textInput = document.getElementById('textInput');
        const activeTab = document.querySelector('.input-tab.tab-active');
        const tabName = activeTab ? activeTab.dataset.tab : 'text';
        
        if (tabName === 'text' && textInput && textInput.value.trim().length < 50) {
            showToast('Vui lòng nhập ít nhất 50 ký tự văn bản!', 'error');
            textInput.focus();
            return;
        }
        
        // Build payload
        let payload = getGenerationPayload();
        
        // If file tab, upload file first
        if (tabName === 'file') {
            const fileInput = document.getElementById('fileInput');
            if (fileInput && fileInput.files && fileInput.files.length) {
                const file = fileInput.files[0];
                try {
                    const uploadResult = await uploadSourceFile(file);
                    setCachedUpload(uploadResult.source_file_id, file.name, file.size);
                    payload = {
                        ...payload,
                        source_type: 'file',
                        source_file_id: uploadResult.source_file_id
                    };
                } catch (err) {
                    showToast(err.message || 'Không thể tải file', 'error');
                    return;
                }
            } else if (cachedSourceFile && cachedSourceFile.id) {
                payload = {
                    ...payload,
                    source_type: 'file',
                    source_file_id: cachedSourceFile.id
                };
            } else {
                showToast('Vui lòng chọn hoặc tải file trước khi tạo câu hỏi', 'error');
                return;
            }
        } else {
            payload.source_type = 'text';
        }
        
        // Show loading state
        if (loadingState) loadingState.classList.remove('hidden');
        if (emptyState) emptyState.classList.add('hidden');
        if (questionsContainer) questionsContainer.classList.add('hidden');
        
        // Disable button and show loading
        const originalContent = generateBtn.innerHTML;
        generateBtn.disabled = true;
        generateBtn.innerHTML = `
            <svg class="w-5 h-5 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
            Đang xử lý...
        `;
        
        try {
            const response = await fetch('/api/generate-mcq/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                },
                body: JSON.stringify(payload)
            });
            
            const data = await response.json();
            
            if (!response.ok || !data.success) {
                throw new Error(data.error || 'Không thể tạo câu hỏi');
            }
            
            showToast('Đã tạo câu hỏi thành công!', 'success');
            
            // Update credits if available
            if (data.user_credits !== undefined) {
                updateUserCredits(data.user_credits);
            }
            
            // Update current subject info if available
            if (data.subject_id) {
                currentSubjectId = data.subject_id;
            }
            if (data.subject) {
                currentSubjectName = data.subject;
            }
            
            // Reload questions for the newly created subject
            if (data.subject_id) {
                await loadQuestionsFromBackend(data.subject_id);
            } else {
                await loadQuestionsFromBackend();
            }
            
            // Refresh history panel
            await refreshHistoryPanel();
            
        } catch (err) {
            console.error(err);
            showToast(err.message || 'Có lỗi khi tạo câu hỏi', 'error');
            // Show empty state back if needed
            if (emptyState) emptyState.classList.remove('hidden');
        } finally {
            // Hide loading
            if (loadingState) loadingState.classList.add('hidden');
            if (questionsContainer) questionsContainer.classList.remove('hidden');
            
            // Restore button
            generateBtn.disabled = false;
            generateBtn.innerHTML = originalContent;
        }
    });
}

/**
 * Difficulty Buttons
 */
function initDifficultyButtons() {
    const difficultyContainer = document.querySelector('.difficulty-container');
    if (!difficultyContainer) {
        // Find difficulty buttons by their structure
        const buttons = document.querySelectorAll('[class*="flex gap-2"] > button[data-level]');
        if (buttons.length >= 3) {
            setupDifficultyButtons(buttons);
        }
    }
}

function setupDifficultyButtons(buttons) {
    const diffInput = document.getElementById('difficultyValue');
    buttons.forEach(btn => {
        btn.addEventListener('click', function() {
            // Reset all buttons
            buttons.forEach(b => {
                b.classList.remove('text-white', 'bg-blue-600', 'shadow-lg', 'shadow-blue-500/30');
                b.classList.add('text-gray-600', 'dark:text-gray-300', 'bg-gray-50', 'dark:bg-gray-700', 'border', 'border-gray-200', 'dark:border-gray-600');
            });
            
            // Activate clicked button
            this.classList.remove('text-gray-600', 'dark:text-gray-300', 'bg-gray-50', 'dark:bg-gray-700', 'border', 'border-gray-200', 'dark:border-gray-600');
            this.classList.add('text-white', 'bg-blue-600', 'shadow-lg', 'shadow-blue-500/30');
            
            // Update hidden difficulty value
            if (diffInput && this.dataset.level) {
                diffInput.value = this.dataset.level;
            }
        });
    });
}

/**
 * Question Type Checkboxes
 */
function initQuestionTypeCheckboxes() {
    const checkboxLabels = document.querySelectorAll('.grid.grid-cols-2.gap-2 > label');
    
    checkboxLabels.forEach(label => {
        const checkbox = label.querySelector('input[type="checkbox"]');
        if (checkbox) {
            // Update initial state
            updateCheckboxStyle(label, checkbox.checked);
            
            checkbox.addEventListener('change', function() {
                updateCheckboxStyle(label, this.checked);
            });
        }
    });
}

function updateCheckboxStyle(label, isChecked) {
    if (isChecked) {
        label.classList.remove('bg-gray-50', 'dark:bg-gray-700', 'border', 'border-gray-200', 'dark:border-gray-600');
        label.classList.add('bg-blue-50', 'dark:bg-blue-900/20', 'border-2', 'border-blue-500');
    } else {
        label.classList.add('bg-gray-50', 'dark:bg-gray-700', 'border', 'border-gray-200', 'dark:border-gray-600');
        label.classList.remove('bg-blue-50', 'dark:bg-blue-900/20', 'border-2', 'border-blue-500');
    }
}

/**
 * Export Functions
 */
function exportToPDF() {
    alert('Đang xuất file PDF...');
    // TODO: Implement PDF export
}

function exportToWord() {
    alert('Đang xuất file Word...');
    // TODO: Implement Word export
}

function exportToExcel() {
    alert('Đang xuất file Excel...');
    // TODO: Implement Excel export
}

function exportToJSON() {
    const data = getQuestionsData();
    
    // Check if there are questions to export
    if (!data.questions || data.questions.length === 0) {
        showToast('Không có câu hỏi nào để xuất!', 'warning');
        return;
    }
    
    const blob = new Blob([JSON.stringify(data, null, 2)], { type: 'application/json' });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    
    // Generate filename with subject name if available
    const subjectName = data.subject ? data.subject.replace(/[^a-zA-Z0-9]/g, '_') : 'questions';
    const timestamp = new Date().toISOString().split('T')[0];
    a.download = `${subjectName}_${timestamp}.json`;
    
    a.click();
    URL.revokeObjectURL(url);
    showToast('Đã xuất file JSON thành công!', 'success');
}

function copyToClipboard() {
    const data = getQuestionsData();
    // Get questions array from the data object
    const questions = data.questions || [];
    const text = formatQuestionsAsText(questions);
    navigator.clipboard.writeText(text).then(() => {
        showToast('Đã sao chép vào clipboard!', 'success');
    }).catch(err => {
        console.error('Lỗi sao chép:', err);
        showToast('Không thể sao chép vào clipboard', 'error');
    });
}

/**
 * Get questions data with subject information for export
 * Returns object with subject info and questions array
 */
function getQuestionsData() {
    // Get subject information - prioritize currentSubjectName (set when loading from history)
    let subject = currentSubjectName || '';
    let subject_id = currentSubjectId;
    
    // If subject name not available, try to get from select or input
    if (!subject) {
        const subjectSelect = document.getElementById('subjectSelect');
        const subjectInput = document.getElementById('subjectInput');
        
        if (subjectSelect && subjectSelect.value === '__new__' && subjectInput) {
            // New subject from input
            subject = subjectInput.value.trim();
            subject_id = null;
        } else if (subjectSelect && subjectSelect.value && subjectSelect.value !== '__new__') {
            // Existing subject from select
            const selectedOption = subjectSelect.options[subjectSelect.selectedIndex];
            if (selectedOption.hasAttribute('data-subject-name')) {
                subject_id = subjectSelect.value.trim();
                subject = selectedOption.getAttribute('data-subject-name');
            } else {
                // Old format: value is the subject name
                subject = subjectSelect.value.trim();
                subject_id = null;
            }
        } else if (subjectInput && !subjectInput.classList.contains('hidden')) {
            // Fallback to input if visible
            subject = subjectInput.value.trim();
            subject_id = null;
        } else if (currentSubjectId) {
            // If we have currentSubjectId but no name, try to find from history items
            subject_id = currentSubjectId;
            
            // Try from history items in DOM
            const historyItem = document.querySelector(`[data-subject-id="${currentSubjectId}"]`);
            if (historyItem) {
                const titleElement = historyItem.querySelector('p.text-sm.font-medium');
                if (titleElement) {
                    subject = titleElement.textContent.trim();
                }
            }
            
            // If still not found and we have currentSubjectName, use it
            if (!subject && currentSubjectName) {
                subject = currentSubjectName;
            }
            
            // Last resort: use subject_id as fallback
            if (!subject) {
                subject = `Subject_${currentSubjectId.substring(0, 8)}`;
            }
        }
    }
    
    // Fallback if still no subject name - try to get from questions if available
    if (!subject && allQuestions.length > 0) {
        // Try to get from first question's metadata if available
        // This is a last resort fallback
        subject = 'Questions';
    } else if (!subject) {
        subject = 'Unknown Subject';
    }
    
    // Get questions from allQuestions array (contains all loaded questions)
    const questions = allQuestions.map(q => {
        // Extract correct answer
        const correctOption = q.options?.find(opt => opt.is_correct);
        const correctAnswer = correctOption ? correctOption.id : null;
        
        return {
            id: q.id,
            stem: q.stem || q.content || '',
            type: 'multiple_choice',
            difficulty: q.difficulty || 'medium',
            bloom_level: q.bloom_level || null,
            options: (q.options || []).map(opt => ({
                id: opt.id,
                text: opt.text || '',
                is_correct: opt.is_correct || false
            })),
            correct_answer: correctAnswer,
            explanation: q.explanation || '',
            user_edited: q.user_edited || false,
            created_at: q.created_at || null,
            updated_at: q.updated_at || null
        };
    });
    
    // Return structured data with subject info
    return {
        subject: subject || 'Unknown',
        subject_id: subject_id,
        export_date: new Date().toISOString(),
        total_questions: questions.length,
        questions: questions
    };
}

function formatQuestionsAsText(questions) {
    if (!questions || questions.length === 0) {
        return 'Không có câu hỏi nào';
    }
    
    return questions.map((q, i) => {
        // Support both old format (question) and new format (stem)
        const questionText = q.stem || q.question || q.content || '';
        let text = `Câu ${i + 1}: ${questionText}\n`;
        
        if (q.options && q.options.length > 0) {
            // Support both old format (array of strings) and new format (array of objects)
            q.options.forEach((opt, j) => {
                const letter = String.fromCharCode(65 + j);
                const optText = typeof opt === 'string' ? opt : (opt.text || opt.id || '');
                // Support both old format (correct as index) and new format (is_correct flag)
                const isCorrect = typeof opt === 'string' 
                    ? (j === q.correct || j === q.correct_answer) 
                    : (opt.is_correct || opt.id === q.correct_answer);
                const marker = isCorrect ? '✓' : ' ';
                text += `  ${letter}. ${optText} ${marker}\n`;
            });
        }
        
        if (q.explanation) {
            text += `\nGiải thích: ${q.explanation}\n`;
        }
        return text;
    }).join('\n---\n\n');
}

/**
 * Add New Question - Open Modal
 */
function addNewQuestion() {
    openAddQuestionModal();
}

/**
 * Open Add Question Modal with enhanced animation
 */
function openAddQuestionModal() {
    const modal = document.getElementById('addQuestionModal');
    if (!modal) return;
    
    const backdrop = modal.querySelector('.modal-backdrop');
    const content = modal.querySelector('.modal-content');
    
    // Show modal
    modal.classList.remove('hidden');
    
    // Trigger animations
    requestAnimationFrame(() => {
        modal.classList.add('show');
        
        if (backdrop) {
            backdrop.style.opacity = '1';
        }
        if (content) {
            content.style.opacity = '1';
            content.style.transform = 'scale(1) translateY(0)';
        }
    });
    
    // Prevent body scroll
    document.body.style.overflow = 'hidden';
    
    // Focus on first input with smooth transition
    setTimeout(() => {
        const firstInput = document.getElementById('newQuestionContent');
        if (firstInput) {
            firstInput.focus();
            firstInput.classList.add('animate-pulse-border');
            setTimeout(() => {
                firstInput.classList.remove('animate-pulse-border');
            }, 2000);
        }
    }, 300);
}

/**
 * Close Add Question Modal with enhanced animation
 */
function closeAddQuestionModal() {
    const modal = document.getElementById('addQuestionModal');
    if (!modal) return;
    
    const backdrop = modal.querySelector('.modal-backdrop');
    const content = modal.querySelector('.modal-content');
    
    // Animate out
    modal.classList.remove('show');
    
    if (backdrop) {
        backdrop.style.opacity = '0';
    }
    if (content) {
        content.style.opacity = '0';
        content.style.transform = 'scale(0.95) translateY(20px)';
    }
    
    // Wait for animation then hide
    setTimeout(() => {
        modal.classList.add('hidden');
        document.body.style.overflow = '';
        
        // Reset styles for next open
        if (backdrop) backdrop.style.opacity = '';
        if (content) {
            content.style.opacity = '';
            content.style.transform = '';
        }
    }, 300);
}

/**
 * Select Correct Answer - Toggle answer button colors
 */
function selectCorrectAnswer(letter) {
    // Update hidden input
    const hiddenInput = document.getElementById('selectedCorrectAnswer');
    if (hiddenInput) {
        hiddenInput.value = letter;
    }
    
    // Update all label buttons
    ['A', 'B', 'C', 'D'].forEach(l => {
        const label = document.getElementById('label' + l);
        if (label) {
            if (l === letter) {
                // Selected - green with shadow
                label.className = 'w-10 h-10 flex-shrink-0 flex items-center justify-center rounded-lg bg-green-500 text-white font-bold cursor-pointer transition-all hover:scale-110 shadow-md shadow-green-500/50';
            } else {
                // Not selected - gray
                label.className = 'w-10 h-10 flex-shrink-0 flex items-center justify-center rounded-lg bg-gray-300 dark:bg-gray-600 text-gray-700 dark:text-gray-300 font-bold cursor-pointer transition-all hover:scale-110';
            }
        }
    });
    
    console.log('Selected correct answer:', letter);
}

/**
 * Reset Add Question Form
 */
function resetAddQuestionForm() {
    // Reset subject select and input in modal
    const modalSubjectSelect = document.getElementById('newQuestionSubjectSelect');
    const modalSubjectInput = document.getElementById('newQuestionSubjectInput');
    if (modalSubjectSelect) {
        modalSubjectSelect.value = '';
        if (modalSubjectInput) {
            modalSubjectInput.classList.add('hidden');
            modalSubjectInput.value = '';
        }
    }
    document.getElementById('newQuestionContent').value = '';
    document.getElementById('optionA').value = '';
    document.getElementById('optionB').value = '';
    document.getElementById('optionC').value = '';
    document.getElementById('optionD').value = '';
    document.getElementById('newQuestionExplanation').value = '';
    document.getElementById('newQuestionBloom').value = 'understand';
    document.getElementById('newQuestionDifficulty').value = 'medium';
    
    // Reset correct answer selection to A
    selectCorrectAnswer('A');
}

/**
 * Submit New Question - Calls Backend API
 */
async function submitNewQuestion() {
    // Get form values
    const content = document.getElementById('newQuestionContent').value.trim();
    const optionA = document.getElementById('optionA').value.trim();
    const optionB = document.getElementById('optionB').value.trim();
    const optionC = document.getElementById('optionC').value.trim();
    const optionD = document.getElementById('optionD').value.trim();
    const explanation = document.getElementById('newQuestionExplanation').value.trim();
    const bloom = document.getElementById('newQuestionBloom')?.value || '';
    const difficulty = document.getElementById('newQuestionDifficulty').value;
    const correctAnswer = document.getElementById('selectedCorrectAnswer')?.value || 'A';
    
    // Get subject and subject_id from modal select or input
    const subjectSelect = document.getElementById('newQuestionSubjectSelect');
    const subjectInput = document.getElementById('newQuestionSubjectInput');
    let subject = '';
    let subject_id = null;
    
    if (subjectSelect && subjectSelect.value === '__new__' && subjectInput) {
        // New subject from input
        subject = subjectInput.value.trim();
        subject_id = null;
    } else if (subjectSelect && subjectSelect.value && subjectSelect.value !== '__new__') {
        // Existing subject from select
        const selectedOption = subjectSelect.options[subjectSelect.selectedIndex];
        // Check if it's new format (has data-subject-name) or old format (value is name)
        if (selectedOption.hasAttribute('data-subject-name')) {
            subject_id = subjectSelect.value.trim();
            subject = selectedOption.getAttribute('data-subject-name');
        } else {
            // Old format: value is the subject name
            subject = subjectSelect.value.trim();
            subject_id = null;
        }
    } else if (subjectInput && !subjectInput.classList.contains('hidden')) {
        // Fallback to input if visible
        subject = subjectInput.value.trim();
        subject_id = null;
    }

    // Validation with animation
    const contentInput = document.getElementById('newQuestionContent');
    if (!content) {
        showToast('Vui lòng nhập nội dung câu hỏi!', 'error');
        contentInput.classList.add('input-error', 'animate-shake');
        contentInput.focus();
        setTimeout(() => {
            contentInput.classList.remove('input-error', 'animate-shake');
        }, 500);
        return;
    }
    
    // Validate options
    const optionInputs = ['optionA', 'optionB', 'optionC', 'optionD'];
    const optionValues = [optionA, optionB, optionC, optionD];
    
    for (let i = 0; i < optionValues.length; i++) {
        if (!optionValues[i]) {
            const input = document.getElementById(optionInputs[i]);
            showToast(`Vui lòng nhập đáp án ${String.fromCharCode(65 + i)}!`, 'error');
            input.classList.add('input-error', 'animate-shake');
            input.focus();
            setTimeout(() => {
                input.classList.remove('input-error', 'animate-shake');
            }, 500);
            return;
        }
    }

    // Create question data for API
    const questionData = {
        content: content,
        options: [
            { id: 'A', text: optionA, is_correct: correctAnswer === 'A' },
            { id: 'B', text: optionB, is_correct: correctAnswer === 'B' },
            { id: 'C', text: optionC, is_correct: correctAnswer === 'C' },
            { id: 'D', text: optionD, is_correct: correctAnswer === 'D' }
        ],
        correct_answer: correctAnswer,
        explanation: explanation,
        bloom_level: bloom,
        difficulty: difficulty,
        subject: subject  // Include subject in request
    };
    
    // Add subject_id if available
    if (subject_id) {
        questionData.subject_id = subject_id;
    }

    // Show loading state on submit button
    const submitBtn = document.querySelector('[onclick="submitNewQuestion()"]');
    const originalContent = submitBtn.innerHTML;
    submitBtn.disabled = true;
    submitBtn.innerHTML = `
        <svg class="w-4 h-4 inline animate-spin" fill="none" viewBox="0 0 24 24">
            <circle class="opacity-25" cx="12" cy="12" r="10" stroke="currentColor" stroke-width="4"></circle>
            <path class="opacity-75" fill="currentColor" d="M4 12a8 8 0 018-8V0C5.373 0 0 5.373 0 12h4z"></path>
        </svg>
        Đang lưu...
    `;

    try {
        const response = await fetch(API_ENDPOINTS.createQuestion, {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(questionData)
        });

        const data = await response.json();

        if (data.success) {
            showToast('Đã thêm câu hỏi mới thành công!', 'success');
            resetAddQuestionForm();
            closeAddQuestionModal();
            
            // Update credits if available
            if (data.user_credits !== undefined) {
                updateUserCredits(data.user_credits);
            }
            
            // Reload questions from backend to avoid duplicates and update history
            await loadQuestionsFromBackend();
            await refreshHistoryPanel();
        } else {
            showToast(data.error || 'Có lỗi xảy ra khi tạo câu hỏi', 'error');
        }
    } catch (error) {
        console.error('Error creating question:', error);
        // Fallback to local-only mode if API fails
        const localQuestion = {
            id: 'local_' + Date.now(),
            content: content,
            options: questionData.options,
            explanation: explanation,
            bloom_level: bloom,
            difficulty: difficulty,
            user_edited: true
        };
        
        // In offline mode, still try to reload from backend
        await loadQuestionsFromBackend();
        await refreshHistoryPanel();
        showToast('Câu hỏi đã được thêm (chế độ offline)', 'warning');
        resetAddQuestionForm();
        closeAddQuestionModal();
    } finally {
        // Restore button state
        submitBtn.disabled = false;
        submitBtn.innerHTML = originalContent;
    }
}

/**
 * Create Question Card HTML
 */
function createQuestionCardHTML(question, orderNum, difficultyLabel) {
    const rawContent = question.stem || question.content || '';
    const displayContent = formatDisplayText(rawContent);
    const hasCode = /```|`|<code>|<pre>/i.test(rawContent);
    const stemExtraClass = hasCode ? 'font-mono text-sm' : '';
    return `
        <div class="question-card animate-card-enter bg-gray-50 dark:bg-gray-700/50 rounded-xl p-5 border dark:border-gray-600 hover-lift" style="border-color: rgba(229, 231, 235, 1);" data-question-id="${question.id}">
            <!-- Question Header -->
            <div class="flex items-start justify-between mb-4">
                <div class="flex items-center gap-2">
                    <span class="text-sm font-semibold text-gray-400 dark:text-gray-500">#${orderNum}</span>
                    <span class="px-2 py-1 text-xs font-medium bg-${difficultyLabel.color}-100 dark:bg-${difficultyLabel.color}-900/30 text-${difficultyLabel.color}-600 dark:text-${difficultyLabel.color}-400 rounded-lg">${difficultyLabel.text}</span>
                    ${question.user_edited ? '<span class="px-2 py-1 text-xs font-medium bg-purple-100 dark:bg-purple-900/30 text-purple-600 dark:text-purple-400 rounded-lg">Thủ công</span>' : '<span class="px-2 py-1 text-xs font-medium bg-green-100 dark:bg-green-900/30 text-green-600 dark:text-green-400 rounded-lg">Tự động</span>'}
                </div>
                <div class="flex items-center gap-1">
                    <button onclick="editQuestion('${question.id}')" class="p-1.5 hover:bg-gray-200 dark:hover:bg-gray-600 rounded-lg transition-smooth" title="Chỉnh sửa">
                        <svg class="w-4 h-4 text-gray-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M11 5H6a2 2 0 00-2 2v11a2 2 0 002 2h11a2 2 0 002-2v-5m-1.414-9.414a2 2 0 112.828 2.828L11.828 15H9v-2.828l8.586-8.586z"/>
                        </svg>
                    </button>
                    <button onclick="deleteQuestion('${question.id}')" class="p-1.5 hover:bg-red-100 dark:hover:bg-red-900/30 rounded-lg transition-smooth" title="Xóa">
                        <svg class="w-4 h-4 text-red-500" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                            <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M19 7l-.867 12.142A2 2 0 0116.138 21H7.862a2 2 0 01-1.995-1.858L5 7m5 4v6m4-6v6m1-10V4a1 1 0 00-1-1h-4a1 1 0 00-1 1v3M4 7h16"/>
                        </svg>
                    </button>
                </div>
            </div>

            <!-- Question Content -->
            <h4 class="text-gray-900 dark:text-white font-medium mb-4 whitespace-pre-wrap break-words ${stemExtraClass} input-animated rounded p-1 -m-1" contenteditable="true" data-field="stem">${escapeHtml(displayContent)}</h4>

            <!-- Options (click to select correct answer) -->
            <div class="space-y-2">
                ${question.options.map(opt => `
                    <div class="option-item flex items-center gap-3 p-3 rounded-lg transition-smooth cursor-pointer hover:shadow-md ${opt.is_correct ? 'bg-green-50 dark:bg-green-900/20 border-2 border-green-500' : 'bg-white dark:bg-gray-700 border border-gray-200 dark:border-gray-600 hover:border-blue-400'}">
                        <span class="w-8 h-8 flex items-center justify-center rounded-lg answer-btn ${opt.is_correct ? 'bg-green-500 text-white animate-success-pop' : 'bg-gray-200 dark:bg-gray-600 text-gray-600 dark:text-gray-300'} font-medium text-sm">${opt.id}</span>
                        <span class="flex-1 text-gray-700 dark:text-gray-300 whitespace-pre-wrap break-words input-animated rounded p-1 -m-1" contenteditable="true" data-field="option-${opt.id}">${escapeHtml(formatDisplayText(opt.text))}</span>
                        ${opt.is_correct ? '<svg class="w-5 h-5 text-green-500 flex-shrink-0 animate-success-pop" fill="currentColor" viewBox="0 0 24 24"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41L9 16.17z"/></svg>' : ''}
                    </div>
                `).join('')}
            </div>

            <!-- Explanation - Always visible for editing -->
            <div class="mt-4 p-3 bg-blue-50 dark:bg-blue-900/20 rounded-lg border border-blue-200 dark:border-blue-800 transition-smooth max-h-32 overflow-y-auto overflow-x-hidden">
                <div class="flex items-start gap-2">
                    <svg class="w-5 h-5 text-blue-500 flex-shrink-0 mt-0.5" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                        <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M13 16h-1v-4h-1m1-4h.01M21 12a9 9 0 11-18 0 9 9 0 0118 0z"/>
                    </svg>
                    <p class="text-sm text-blue-700 dark:text-blue-300 whitespace-pre-wrap break-words input-animated rounded p-1 -m-1" contenteditable="true" data-field="explanation">${escapeHtml(formatDisplayText(question.explanation || ''))}</p>
                </div>
            </div>
        </div>
    `;
}

/**
 * Add Question to UI
 */
function addQuestionToUI(question) {
    const container = document.getElementById('questionsContainer');
    const emptyState = document.getElementById('emptyState');
    
    if (!container) return;

    // Hide empty state with animation
    if (emptyState) {
        emptyState.style.opacity = '0';
        emptyState.style.transform = 'scale(0.95)';
        setTimeout(() => {
            emptyState.classList.add('hidden');
            emptyState.style.opacity = '';
            emptyState.style.transform = '';
        }, 200);
    }
    container.classList.remove('hidden');

    const difficultyLabels = {
        'easy': { text: 'Easy', color: 'green' },
        'medium': { text: 'Medium', color: 'blue' },
        'hard': { text: 'Hard', color: 'red' }
    };
    const difficultyKey = (question.difficulty || 'medium').toLowerCase();
    const difficultyLabel = difficultyLabels[difficultyKey] || difficultyLabels['medium'];

    // Calculate order number
    const orderNum = document.querySelectorAll('.question-card').length + 1;
    
    // Create and insert question card
    const questionHTML = createQuestionCardHTML(question, orderNum, difficultyLabel);
    container.insertAdjacentHTML('beforeend', questionHTML);

    // Save original data immediately after rendering for cancel functionality
    originalQuestionData.set(question.id, {
        stem: question.content || question.stem || '',
        explanation: question.explanation || '',
        options: (question.options || []).map(opt => ({
            id: opt.id,
            text: opt.text || '',
            is_correct: opt.is_correct || false
        }))
    });

    // Update question count with animation
    updateQuestionCount();
    
    // Scroll to new question
    const newCard = container.lastElementChild;
    if (newCard) {
        setTimeout(() => {
            newCard.scrollIntoView({ behavior: 'smooth', block: 'center' });
        }, 100);
    }
}

/**
 * Show Toast Notification with enhanced animation
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
 * Close Toast with animation
 */
function closeToast(toast) {
    if (!toast || !toast.parentElement) return;
    
    toast.style.opacity = '0';
    toast.style.transform = 'translateX(100%)';
    setTimeout(() => toast.remove(), 300);
}

/**
 * Escape HTML to prevent XSS
 */
function escapeHtml(text) {
    const div = document.createElement('div');
    div.textContent = text;
    return div.innerHTML;
}

// Normalize text for display: convert <br> to newline
function formatDisplayText(text) {
    if (!text) return '';
    return String(text).replace(/<br\s*\/?>/gi, '\n');
}

/**
 * Edit Question - Show update button
 */
function editQuestion(questionId) {
    const card = document.querySelector(`[data-question-id="${questionId}"]`);
    if (!card) return;
    
    // Toggle edit mode - highlight editable fields
    const editableFields = card.querySelectorAll('[contenteditable="true"]');
    editableFields.forEach(field => {
        field.classList.add('ring-2', 'ring-blue-500', 'bg-blue-50', 'dark:bg-blue-900/20');
    });
    
    // Show update button if not already visible
    let updateBtn = card.querySelector('.update-btn');
    if (!updateBtn) {
        const actionsDiv = card.querySelector('.flex.items-center.gap-1');
        if (actionsDiv) {
            const btn = document.createElement('button');
            btn.className = 'update-btn p-1.5 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-smooth';
            btn.title = 'Lưu thay đổi';
            btn.onclick = () => updateQuestion(questionId);
            btn.innerHTML = `
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
            `;
            actionsDiv.insertBefore(btn, actionsDiv.firstChild);
        }
    }
    
    showToast('Chỉnh sửa nội dung, click đáp án để chọn đáp án đúng, nhấn ✓ để lưu', 'info');
}

/**
 * Update Question - Save changes to backend
 */
async function updateQuestion(questionId) {
    const card = document.querySelector(`[data-question-id="${questionId}"]`);
    if (!card) return;
    
    // Get updated values from contenteditable fields
    const stemField = card.querySelector('[data-field="stem"]');
    const explanationField = card.querySelector('[data-field="explanation"]');
    const optionFields = card.querySelectorAll('[data-field^="option-"]');
    
    const content = stemField ? stemField.textContent.trim() : '';
    const explanation = explanationField ? explanationField.textContent.trim() : '';
    
    // Build options array
    const options = [];
    optionFields.forEach(field => {
        const optId = field.dataset.field.replace('option-', '');
        const optItem = field.closest('.option-item');
        const isCorrect = optItem ? optItem.classList.contains('border-green-500') || optItem.classList.contains('bg-green-50') : false;
        options.push({
            id: optId,
            text: field.textContent.trim(),
            is_correct: isCorrect
        });
    });
    
    // Find correct answer
    const correctAnswer = options.find(opt => opt.is_correct)?.id || 'A';
    
    // Show loading
    const updateBtn = card.querySelector('.update-btn');
    if (updateBtn) {
        updateBtn.disabled = true;
        updateBtn.innerHTML = `
            <svg class="w-4 h-4 animate-spin" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M4 4v5h.582m15.356 2A8.001 8.001 0 004.582 9m0 0H9m11 11v-5h-.581m0 0a8.003 8.003 0 01-15.357-2m15.357 2H15"/>
            </svg>
        `;
    }
    
    try {
        // Skip API call for local questions
        if (questionId.startsWith('local_')) {
            showToast('Câu hỏi đã được cập nhật (local)', 'success');
            removeEditHighlight(card);
            return;
        }
        
        const response = await fetch(API_ENDPOINTS.updateQuestion(questionId), {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                content: content,
                options: options,
                correct_answer: correctAnswer,
                explanation: explanation
            })
        });
        
        const data = await response.json();
        
        if (data.success) {
            showToast('Đã lưu thay đổi!', 'success');
            removeEditHighlight(card);
        } else {
            showToast(data.error || 'Không thể cập nhật', 'error');
        }
    } catch (error) {
        console.error('Error updating question:', error);
        showToast('Lỗi khi cập nhật câu hỏi', 'error');
    } finally {
        // Restore button
        if (updateBtn) {
            updateBtn.disabled = false;
            updateBtn.innerHTML = `
                <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                    <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
                </svg>
            `;
        }
    }
}

// Store original data for cancel functionality
const originalQuestionData = new Map();

/**
 * Save original question data before editing
 * This should be called BEFORE any changes are made
 */
function saveOriginalData(card) {
    const questionId = card.dataset.questionId;
    if (!questionId || originalQuestionData.has(questionId)) return;
    
    const stemField = card.querySelector('[data-field="stem"]');
    const explanationField = card.querySelector('[data-field="explanation"]');
    const optionItems = card.querySelectorAll('.option-item');
    
    const options = [];
    optionItems.forEach(optItem => {
        const optField = optItem.querySelector('[data-field^="option-"]');
        const optId = optField ? optField.dataset.field.replace('option-', '') : '';
        const isCorrect = optItem.classList.contains('border-green-500') || optItem.classList.contains('bg-green-50');
        options.push({
            id: optId,
            text: optField ? optField.textContent.trim() : '',
            is_correct: isCorrect
        });
    });
    
    originalQuestionData.set(questionId, {
        stem: stemField ? stemField.textContent.trim() : '',
        explanation: explanationField ? explanationField.textContent.trim() : '',
        options: options
    });
}

// Save original data when user focuses on editable field (BEFORE any changes)
document.addEventListener('focusin', function(e) {
    if (e.target.matches('[contenteditable="true"]')) {
        const card = e.target.closest('.question-card');
        if (card) {
            saveOriginalData(card);
        }
    }
});

// Save original data when user is about to click on option (BEFORE any changes)
document.addEventListener('mousedown', function(e) {
    const optItem = e.target.closest('.option-item');
    if (optItem) {
        const card = optItem.closest('.question-card');
        if (card) {
            saveOriginalData(card);
        }
    }
});

/**
 * Cancel edit and restore original data
 */
function cancelEdit(questionId) {
    const card = document.querySelector(`[data-question-id="${questionId}"]`);
    if (!card) return;
    
    const originalData = originalQuestionData.get(questionId);
    if (originalData) {
        // Restore stem
        const stemField = card.querySelector('[data-field="stem"]');
        if (stemField) {
            stemField.textContent = originalData.stem;
        }
        
        // Restore explanation
        const explanationField = card.querySelector('[data-field="explanation"]');
        if (explanationField) {
            explanationField.textContent = originalData.explanation;
        }
        
        // Restore options text and correct answer styling
        originalData.options.forEach(opt => {
            const optField = card.querySelector(`[data-field="option-${opt.id}"]`);
            if (optField) {
                optField.textContent = opt.text;
            }
            
            // Restore correct answer styling using helper
            const optItem = optField ? optField.closest('.option-item') : null;
            if (optItem) {
                setOptionStyle(optItem, opt.is_correct);
            }
        });
        
        // Clear saved data
        originalQuestionData.delete(questionId);
    }
    
    removeEditHighlight(card);
    showToast('Đã hủy thay đổi', 'info');
}

/**
 * Remove edit highlight from card
 */
function removeEditHighlight(card) {
    const editableFields = card.querySelectorAll('[contenteditable="true"]');
    editableFields.forEach(field => {
        field.classList.remove('ring-2', 'ring-blue-500', 'bg-blue-50', 'dark:bg-blue-900/20');
    });
    
    // Remove update button
    const updateBtn = card.querySelector('.update-btn');
    if (updateBtn) {
        updateBtn.remove();
    }
    
    // Remove cancel button
    const cancelBtn = card.querySelector('.cancel-btn');
    if (cancelBtn) {
        cancelBtn.remove();
    }
    
    // Clear original data
    const questionId = card.dataset.questionId;
    if (questionId) {
        originalQuestionData.delete(questionId);
    }
}

/**
 * Show update and cancel buttons when content changes
 */
function showUpdateButtonOnChange(card) {
    const questionId = card.dataset.questionId;
    if (!questionId) return;
    
    // Check if buttons already exist
    let updateBtn = card.querySelector('.update-btn');
    if (updateBtn) return;
    
    const actionsDiv = card.querySelector('.flex.items-center.gap-1');
    if (actionsDiv) {
        // Add Update button
        const btn = document.createElement('button');
        btn.className = 'update-btn p-1.5 bg-green-500 hover:bg-green-600 text-white rounded-lg transition-smooth animate-success-pop';
        btn.title = 'Lưu thay đổi';
        btn.onclick = () => updateQuestion(questionId);
        btn.innerHTML = `
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M5 13l4 4L19 7"/>
            </svg>
        `;
        actionsDiv.insertBefore(btn, actionsDiv.firstChild);
        
        // Add Cancel button
        const cancelBtnEl = document.createElement('button');
        cancelBtnEl.className = 'cancel-btn p-1.5 bg-gray-400 hover:bg-gray-500 text-white rounded-lg transition-smooth animate-success-pop';
        cancelBtnEl.title = 'Hủy thay đổi';
        cancelBtnEl.onclick = () => cancelEdit(questionId);
        cancelBtnEl.innerHTML = `
            <svg class="w-4 h-4" fill="none" stroke="currentColor" viewBox="0 0 24 24">
                <path stroke-linecap="round" stroke-linejoin="round" stroke-width="2" d="M6 18L18 6M6 6l12 12"/>
            </svg>
        `;
        actionsDiv.insertBefore(cancelBtnEl, btn.nextSibling);
    }
}

// Listen for content changes in question cards
document.addEventListener('input', function(e) {
    if (e.target.matches('[contenteditable="true"]')) {
        const card = e.target.closest('.question-card');
        if (card) {
            showUpdateButtonOnChange(card);
        }
    }
});

/**
 * Select correct answer by clicking on option
 */
function selectCorrectOption(card, optionId) {
    if (!card) return;
    
    const options = card.querySelectorAll('.option-item');
    
    options.forEach(optItem => {
        const optField = optItem.querySelector('[data-field^="option-"]');
        const currentOptId = optField ? optField.dataset.field.replace('option-', '') : '';
        setOptionStyle(optItem, currentOptId === optionId);
    });
    
    // Show update button
    showUpdateButtonOnChange(card);
}

// Listen for clicks on option items to change correct answer
document.addEventListener('click', function(e) {
    const optItem = e.target.closest('.option-item');
    if (!optItem) return;
    
    // Don't trigger if clicking on contenteditable text
    if (e.target.matches('[contenteditable="true"]')) return;
    
    const card = optItem.closest('.question-card');
    if (!card) return;
    
    const optField = optItem.querySelector('[data-field^="option-"]');
    if (!optField) return;
    
    const optionId = optField.dataset.field.replace('option-', '');
    selectCorrectOption(card, optionId);
});

// Close modal on backdrop click (scoped to modal only to avoid accidental close)
document.addEventListener('click', function(e) {
    const modal = document.getElementById('addQuestionModal');
    if (!modal || modal.classList.contains('hidden')) return;
    
    // Only close when clicking directly on backdrop (not on content)
    if (e.target.classList.contains('modal-backdrop')) {
        closeAddQuestionModal();
    }
});

// Close modal on Escape key
document.addEventListener('keydown', function(e) {
    if (e.key === 'Escape') {
        closeAddQuestionModal();
    }
});

/**
 * Delete Question - With Backend API
 */
async function deleteQuestion(questionId) {
    if (!confirm('Bạn có chắc muốn xóa câu hỏi này?')) {
        return;
    }
    
    const questionCard = document.querySelector(`[data-question-id="${questionId}"]`);
    if (!questionCard) return;
    
    // Add exit animation
    questionCard.classList.add('animate-card-exit');
    
    try {
        // Try to delete from backend if it's a real ID (UUID)
        if (!questionId.startsWith('local_')) {
            const response = await fetch(API_ENDPOINTS.deleteQuestion(questionId), {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': getCsrfToken()
                }
            });
            
            const data = await response.json();
            
            if (!data.success) {
                console.warn('Backend delete failed:', data.error);
            }
        }
    } catch (error) {
        console.log('Could not delete from backend:', error);
    }
    
    // Remove from UI after animation
    setTimeout(() => {
        questionCard.remove();
        updateQuestionCount();
        reorderQuestionNumbers();
        
        // Show empty state if no questions left
        const remainingQuestions = document.querySelectorAll('.question-card');
        if (remainingQuestions.length === 0) {
            const emptyState = document.getElementById('emptyState');
            const container = document.getElementById('questionsContainer');
            if (emptyState) {
                emptyState.classList.remove('hidden');
                emptyState.style.opacity = '0';
                setTimeout(() => {
                    emptyState.style.opacity = '1';
                }, 10);
            }
            if (container) container.classList.add('hidden');
        }
        
        showToast('Đã xóa câu hỏi', 'success');
    }, 300);
}

/**
 * Reorder Question Numbers after deletion
 */
function reorderQuestionNumbers() {
    const questionCards = document.querySelectorAll('.question-card');
    questionCards.forEach((card, index) => {
        const numberSpan = card.querySelector('.text-gray-400, .dark\\:text-gray-500');
        if (numberSpan) {
            numberSpan.textContent = `#${index + 1}`;
        }
    });
}

/**
 * Regenerate Question
 */
function regenerateQuestion(questionId) {
    alert('Đang tạo lại câu hỏi...');
    // TODO: Implement regenerate question
}

/**
 * Update Question Count
 */
function updateQuestionCount() {
    const questionCount = document.getElementById('questionCount');
    if (questionCount) {
        // Count from allQuestions array instead of DOM elements
        // This ensures we show the total count of all loaded questions, not just visible ones
        const totalCount = allQuestions.length;
        questionCount.textContent = totalCount;
    }
}
