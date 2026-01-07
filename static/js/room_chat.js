/**
 * Room Chat JavaScript Handler
 * Handles real-time messaging, file uploads, typing indicators, and bot interactions
 */

class RoomChatManager {
    constructor(roomId) {
        this.roomId = roomId;
        this.pollingInterval = null;
        this.lastMessageId = 0;
        this.typingTimeout = null;
        this.isTyping = false;
    }

    /**
     * Initialize the chat manager
     */
    init() {
        this.startPolling();
        this.bindEvents();
        console.log('RoomChatManager initialized for room:', this.roomId);
    }

    /**
     * Start polling for new messages
     */
    startPolling() {
        // Poll every 2 seconds
        this.pollingInterval = setInterval(() => {
            this.fetchNewMessages();
            this.fetchMemberStatus();
        }, 2000);
    }

    /**
     * Stop polling
     */
    stopPolling() {
        if (this.pollingInterval) {
            clearInterval(this.pollingInterval);
            this.pollingInterval = null;
        }
    }

    /**
     * Fetch new messages from API
     */
    async fetchNewMessages() {
        try {
            const response = await fetch(`/api/rooms/${this.roomId}/messages/?after=${this.lastMessageId}`, {
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            if (!response.ok) return;

            const data = await response.json();
            if (data.messages && data.messages.length > 0) {
                this.appendMessages(data.messages);
                this.lastMessageId = data.messages[data.messages.length - 1].id;
            }
        } catch (error) {
            console.error('Error fetching messages:', error);
        }
    }

    /**
     * Fetch member status updates
     */
    async fetchMemberStatus() {
        try {
            const response = await fetch(`/api/rooms/${this.roomId}/members/`, {
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            if (!response.ok) return;

            const data = await response.json();
            this.updateMemberList(data.members);
            this.updateTypingIndicator(data.typing_users);
        } catch (error) {
            console.error('Error fetching member status:', error);
        }
    }

    /**
     * Send a message
     */
    async sendMessage(content, file = null) {
        const formData = new FormData();
        formData.append('content', content);
        if (file) {
            formData.append('file', file);
        }

        try {
            const response = await fetch(`/api/rooms/${this.roomId}/messages/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to send message');
            }

            return await response.json();
        } catch (error) {
            console.error('Error sending message:', error);
            throw error;
        }
    }

    /**
     * Upload a file
     */
    async uploadFile(file) {
        const formData = new FormData();
        formData.append('file', file);

        try {
            const response = await fetch(`/api/rooms/${this.roomId}/files/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: formData
            });

            if (!response.ok) {
                throw new Error('Failed to upload file');
            }

            return await response.json();
        } catch (error) {
            console.error('Error uploading file:', error);
            throw error;
        }
    }

    /**
     * Toggle bot status
     */
    async toggleBot(enabled) {
        try {
            const response = await fetch(`/api/rooms/${this.roomId}/bot/toggle/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ enabled })
            });

            if (!response.ok) {
                throw new Error('Failed to toggle bot');
            }

            return await response.json();
        } catch (error) {
            console.error('Error toggling bot:', error);
            throw error;
        }
    }

    /**
     * Send typing indicator
     */
    async sendTypingIndicator() {
        if (this.isTyping) return;

        this.isTyping = true;

        try {
            await fetch(`/api/rooms/${this.roomId}/typing/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });
        } catch (error) {
            console.error('Error sending typing indicator:', error);
        }

        // Reset typing status after 3 seconds
        if (this.typingTimeout) {
            clearTimeout(this.typingTimeout);
        }
        this.typingTimeout = setTimeout(() => {
            this.isTyping = false;
        }, 3000);
    }

    /**
     * Pin/unpin a message
     */
    async togglePinMessage(messageId) {
        try {
            const response = await fetch(`/api/rooms/${this.roomId}/messages/${messageId}/pin/`, {
                method: 'POST',
                headers: {
                    'X-CSRFToken': this.getCsrfToken()
                }
            });

            if (!response.ok) {
                throw new Error('Failed to pin message');
            }

            return await response.json();
        } catch (error) {
            console.error('Error pinning message:', error);
            throw error;
        }
    }

    /**
     * Chat with file (RAG mode)
     */
    async chatWithFile(fileId, question) {
        try {
            const response = await fetch(`/api/rooms/${this.roomId}/files/${fileId}/chat/`, {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({ question })
            });

            if (!response.ok) {
                throw new Error('Failed to chat with file');
            }

            return await response.json();
        } catch (error) {
            console.error('Error chatting with file:', error);
            throw error;
        }
    }

    /**
     * Append messages to the chat container
     */
    appendMessages(messages) {
        const container = document.getElementById('messagesContainer');
        if (!container) return;

        messages.forEach(msg => {
            const messageEl = this.createMessageElement(msg);
            container.appendChild(messageEl);
        });

        // Scroll to bottom
        container.scrollTop = container.scrollHeight;
    }

    /**
     * Create a message element
     */
    createMessageElement(msg) {
        const div = document.createElement('div');
        div.className = msg.is_mine ? 'flex justify-end mb-4' : 'flex justify-start mb-4';

        const bubbleClass = msg.is_mine
            ? 'bg-indigo-600 text-white rounded-2xl rounded-br-md'
            : msg.is_bot
                ? 'bg-indigo-100 dark:bg-indigo-900/30 text-indigo-900 dark:text-indigo-100 rounded-2xl rounded-bl-md'
                : 'bg-white dark:bg-gray-800 text-gray-900 dark:text-white rounded-2xl rounded-bl-md shadow-sm';

        div.innerHTML = `
            <div class="max-w-lg px-4 py-3 ${bubbleClass}">
                ${!msg.is_mine ? `<p class="text-xs font-semibold mb-1 ${msg.is_bot ? 'text-indigo-600' : 'text-gray-500'}">${msg.is_bot ? '🤖 Bot' : msg.sender}</p>` : ''}
                <p class="whitespace-pre-wrap">${this.formatMessage(msg.content)}</p>
                <p class="text-xs mt-1 opacity-70">${msg.time}</p>
            </div>
        `;

        return div;
    }

    /**
     * Format message content (mentions, links, etc.)
     */
    formatMessage(content) {
        // Format @mentions
        content = content.replace(/@(\w+)/g, '<span class="text-indigo-400 font-medium">@$1</span>');

        // Format URLs
        content = content.replace(/(https?:\/\/[^\s]+)/g, '<a href="$1" target="_blank" class="underline">$1</a>');

        return content;
    }

    /**
     * Update member list in sidebar
     */
    updateMemberList(members) {
        // This would be handled by Alpine.js in the template
        // Just dispatch a custom event
        window.dispatchEvent(new CustomEvent('membersUpdated', { detail: members }));
    }

    /**
     * Update typing indicator
     */
    updateTypingIndicator(typingUsers) {
        window.dispatchEvent(new CustomEvent('typingUpdated', { detail: typingUsers }));
    }

    /**
     * Bind event listeners
     */
    bindEvents() {
        // Listen for page unload to stop polling
        window.addEventListener('beforeunload', () => {
            this.stopPolling();
        });

        // Listen for visibility change to pause/resume polling
        document.addEventListener('visibilitychange', () => {
            if (document.hidden) {
                this.stopPolling();
            } else {
                this.startPolling();
            }
        });
    }

    /**
     * Get CSRF token
     */
    getCsrfToken() {
        const cookieValue = document.cookie
            .split('; ')
            .find(row => row.startsWith('csrftoken='))
            ?.split('=')[1];

        return cookieValue || document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';
    }

    /**
     * Destroy the manager
     */
    destroy() {
        this.stopPolling();
    }
}

// Export for use
window.RoomChatManager = RoomChatManager;

// Initialize when DOM is ready
document.addEventListener('DOMContentLoaded', function () {
    // Check if we're on a chat room page
    const roomContainer = document.querySelector('[data-room-id]');
    if (roomContainer) {
        const roomId = roomContainer.dataset.roomId;
        window.chatManager = new RoomChatManager(roomId);
        window.chatManager.init();
    }
});
