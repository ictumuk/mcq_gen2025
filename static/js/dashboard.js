/**
 * Dashboard Controller
 * Handles dashboard-specific functionality
 * Requires: helper.js to be loaded first
 */

// API Configuration for dashboard
const DASHBOARD_API_ENDPOINTS = {
    getQuestions: '/api/questions/',
    deleteSubject: (id) => `/api/subjects/${id}/delete/`
};

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
            // Display questions using shared helper function
            data.questions.forEach((question, index) => {
                const difficultyLabel = getDifficultyLabel(question.difficulty);
                const questionHTML = createReadOnlyQuestionCardHTML(question, index + 1, difficultyLabel);
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
document.addEventListener('keydown', function (event) {
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
        const response = await fetch(DASHBOARD_API_ENDPOINTS.deleteSubject(id), {
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
