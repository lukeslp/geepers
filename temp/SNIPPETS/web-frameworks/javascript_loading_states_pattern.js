/**
 * Loading States and Error Handling Pattern for API Calls
 *
 * Description: Robust pattern for managing loading states, error handling,
 * and success feedback in frontend applications.
 *
 * Use Cases:
 * - Form submissions with async processing
 * - File uploads with progress indication
 * - API calls with loading spinners
 * - Multi-step workflows with state tracking
 *
 * Dependencies:
 * - None (vanilla JavaScript)
 *
 * Notes:
 * - Always use try/finally to ensure loading state is cleared
 * - Show user-friendly error messages
 * - Provide success feedback
 * - Disable buttons during processing to prevent double-submit
 *
 * Related Snippets:
 * - fetch_with_retry.js
 * - form_validation.js
 * - toast_notifications.js
 */

// ============================================================================
// BASIC PATTERN: Single Loading State
// ============================================================================

async function sendMessage() {
    const input = document.getElementById('message-input');
    const loadingEl = document.getElementById('loading');
    const statusEl = document.getElementById('status');
    const submitBtn = document.getElementById('submit-btn');

    const message = input.value.trim();
    if (!message) {
        showStatus(statusEl, 'error', 'Message cannot be empty');
        return;
    }

    // Show loading state
    loadingEl.classList.add('visible');
    submitBtn.disabled = true;
    statusEl.classList.remove('visible'); // Clear previous status

    try {
        const response = await fetch('/api/chat', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ message })
        });

        const data = await response.json();

        if (response.ok) {
            // Success
            displayMessage(data.response);
            input.value = '';
            showStatus(statusEl, 'success', '✅ Message sent!');
        } else {
            // API error
            showStatus(statusEl, 'error', `❌ ${data.error || 'Request failed'}`);
        }

    } catch (error) {
        // Network or other error
        showStatus(statusEl, 'error', `❌ ${error.message}`);
        console.error('Error:', error);

    } finally {
        // Always hide loading state
        loadingEl.classList.remove('visible');
        submitBtn.disabled = false;
    }
}

// ============================================================================
// ADVANCED PATTERN: Multiple Loading States with Progress
// ============================================================================

class LoadingStateManager {
    constructor() {
        this.states = new Map(); // Track multiple concurrent operations
    }

    /**
     * Start a loading operation
     * @param {string} id - Unique identifier for this operation
     * @param {string} message - Loading message to display
     */
    start(id, message = 'Loading...') {
        this.states.set(id, { message, startTime: Date.now() });
        this.render();
    }

    /**
     * Update loading message
     */
    update(id, message) {
        const state = this.states.get(id);
        if (state) {
            state.message = message;
            this.render();
        }
    }

    /**
     * Stop a loading operation
     */
    stop(id) {
        this.states.delete(id);
        this.render();
    }

    /**
     * Render loading indicators
     */
    render() {
        const loadingContainer = document.getElementById('loading-container');
        if (!loadingContainer) return;

        if (this.states.size === 0) {
            loadingContainer.innerHTML = '';
            loadingContainer.classList.remove('visible');
            return;
        }

        loadingContainer.classList.add('visible');
        loadingContainer.innerHTML = Array.from(this.states.entries())
            .map(([id, state]) => `
                <div class="loading-item" data-id="${id}">
                    <div class="spinner"></div>
                    <span>${state.message}</span>
                    <span class="duration">${this.formatDuration(state.startTime)}</span>
                </div>
            `).join('');
    }

    formatDuration(startTime) {
        const seconds = Math.floor((Date.now() - startTime) / 1000);
        return `${seconds}s`;
    }
}

// Global instance
const loadingManager = new LoadingStateManager();

// Usage example
async function generateImage() {
    const operationId = 'image-gen-' + Date.now();

    loadingManager.start(operationId, 'Generating your image...');

    try {
        const response = await fetch('/api/generate-image', {
            method: 'POST',
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({ prompt: 'A mountain landscape' })
        });

        loadingManager.update(operationId, 'Processing image...');

        const data = await response.json();

        if (response.ok) {
            displayImage(data.image);
            showToast('Image generated successfully!', 'success');
        } else {
            showToast(data.error || 'Failed to generate image', 'error');
        }

    } catch (error) {
        showToast(error.message, 'error');
    } finally {
        loadingManager.stop(operationId);
    }
}

// ============================================================================
// HELPER FUNCTIONS
// ============================================================================

/**
 * Show status message
 * @param {HTMLElement} element - Status element
 * @param {string} type - 'success' or 'error'
 * @param {string} message - Status message
 */
function showStatus(element, type, message) {
    element.className = `status visible ${type}`;
    element.textContent = message;

    // Auto-hide after 5 seconds
    setTimeout(() => {
        element.classList.remove('visible');
    }, 5000);
}

/**
 * Show toast notification
 */
function showToast(message, type = 'info') {
    const toast = document.createElement('div');
    toast.className = `toast toast-${type}`;
    toast.textContent = message;

    document.body.appendChild(toast);

    // Fade in
    setTimeout(() => toast.classList.add('visible'), 10);

    // Remove after 3 seconds
    setTimeout(() => {
        toast.classList.remove('visible');
        setTimeout(() => toast.remove(), 300);
    }, 3000);
}

/**
 * Fetch with timeout
 */
async function fetchWithTimeout(url, options = {}, timeout = 30000) {
    const controller = new AbortController();
    const timeoutId = setTimeout(() => controller.abort(), timeout);

    try {
        const response = await fetch(url, {
            ...options,
            signal: controller.signal
        });
        clearTimeout(timeoutId);
        return response;
    } catch (error) {
        clearTimeout(timeoutId);
        if (error.name === 'AbortError') {
            throw new Error('Request timeout');
        }
        throw error;
    }
}

// ============================================================================
// FILE UPLOAD WITH PROGRESS
// ============================================================================

async function uploadFileWithProgress(file, endpoint) {
    const progressBar = document.getElementById('upload-progress');
    const progressText = document.getElementById('upload-progress-text');

    progressBar.style.width = '0%';
    progressBar.parentElement.classList.add('visible');

    try {
        const formData = new FormData();
        formData.append('file', file);

        const xhr = new XMLHttpRequest();

        // Track upload progress
        xhr.upload.addEventListener('progress', (e) => {
            if (e.lengthComputable) {
                const percent = (e.loaded / e.total) * 100;
                progressBar.style.width = percent + '%';
                progressText.textContent = `Uploading: ${Math.round(percent)}%`;
            }
        });

        // Create promise for XHR
        const response = await new Promise((resolve, reject) => {
            xhr.addEventListener('load', () => {
                if (xhr.status >= 200 && xhr.status < 300) {
                    resolve(JSON.parse(xhr.responseText));
                } else {
                    reject(new Error(`Upload failed: ${xhr.status}`));
                }
            });

            xhr.addEventListener('error', () => {
                reject(new Error('Upload failed'));
            });

            xhr.open('POST', endpoint);
            xhr.send(formData);
        });

        progressText.textContent = 'Upload complete!';
        return response;

    } catch (error) {
        progressText.textContent = 'Upload failed';
        throw error;

    } finally {
        // Hide progress bar after 2 seconds
        setTimeout(() => {
            progressBar.parentElement.classList.remove('visible');
        }, 2000);
    }
}

// ============================================================================
// BUTTON STATES
// ============================================================================

class ButtonState {
    constructor(buttonId) {
        this.button = document.getElementById(buttonId);
        this.originalText = this.button.textContent;
    }

    loading(message = 'Loading...') {
        this.button.disabled = true;
        this.button.classList.add('loading');
        this.button.textContent = message;
    }

    success(message = '✅ Success!') {
        this.button.disabled = false;
        this.button.classList.remove('loading');
        this.button.classList.add('success');
        this.button.textContent = message;

        // Reset after 2 seconds
        setTimeout(() => this.reset(), 2000);
    }

    error(message = '❌ Error') {
        this.button.disabled = false;
        this.button.classList.remove('loading');
        this.button.classList.add('error');
        this.button.textContent = message;

        // Reset after 3 seconds
        setTimeout(() => this.reset(), 3000);
    }

    reset() {
        this.button.disabled = false;
        this.button.classList.remove('loading', 'success', 'error');
        this.button.textContent = this.originalText;
    }
}

// Usage
const submitButton = new ButtonState('submit-btn');

async function handleSubmit() {
    submitButton.loading('Sending...');

    try {
        const response = await fetch('/api/submit', { method: 'POST' });
        if (response.ok) {
            submitButton.success('Sent!');
        } else {
            submitButton.error('Failed');
        }
    } catch (error) {
        submitButton.error('Error');
    }
}

// ============================================================================
// CSS REQUIREMENTS
// ============================================================================

/*
.loading {
    display: none;
    align-items: center;
    gap: 0.5rem;
}

.loading.visible {
    display: flex;
}

.spinner {
    width: 24px;
    height: 24px;
    border: 3px solid #f3f3f3;
    border-top: 3px solid #333;
    border-radius: 50%;
    animation: spin 1s linear infinite;
}

@keyframes spin {
    to { transform: rotate(360deg); }
}

.status {
    display: none;
    padding: 1rem;
    border-radius: 4px;
}

.status.visible {
    display: block;
}

.status.success {
    background: #d4edda;
    color: #155724;
}

.status.error {
    background: #f8d7da;
    color: #721c24;
}

.toast {
    position: fixed;
    bottom: 20px;
    right: 20px;
    padding: 1rem;
    border-radius: 4px;
    opacity: 0;
    transition: opacity 0.3s;
}

.toast.visible {
    opacity: 1;
}
*/
