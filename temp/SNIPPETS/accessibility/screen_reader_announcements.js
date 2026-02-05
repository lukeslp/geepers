/**
 * Screen Reader Announcement Patterns
 *
 * Description: Comprehensive patterns for dynamically announcing content changes
 * to screen readers using ARIA live regions. Essential for accessible SPAs and
 * dynamic web applications where content updates without page reloads.
 *
 * Use Cases:
 * - Single Page Applications (SPAs) with dynamic content updates
 * - Form validation messages
 * - Status messages (success, error, info)
 * - Loading states and async operation completion
 * - Dynamic search results or filtering
 * - Toast notifications and alerts
 * - Real-time data updates (chat, notifications, live scores)
 *
 * Dependencies:
 * - Modern browser with ARIA support
 * - DOM manipulation capabilities
 *
 * Notes:
 * - Uses aria-live regions for non-intrusive announcements
 * - Supports different politeness levels (polite, assertive, off)
 * - Announcement elements are cleaned up automatically
 * - Works with all major screen readers (NVDA, JAWS, VoiceOver, TalkBack)
 * - Minimal visual footprint (sr-only class hides announcements)
 * - Can be used standalone or integrated into frameworks
 *
 * ARIA Live Region Politeness Levels:
 * - "polite": Announces when screen reader is idle (non-urgent updates)
 * - "assertive": Interrupts current speech (urgent alerts, errors)
 * - "off": No announcement (default for regular content)
 *
 * Related Snippets:
 * - accessibility/accessible_theme_switcher.js - Theme changes with announcements
 * - accessibility/keyboard_navigation_pattern.js - Focus management
 * - utilities/toast_notification_manager.js - Visual + audible notifications
 *
 * Source Attribution:
 * - Extracted from: /home/coolhand/html/accessibility/index.html
 * - Author: Luke Steuber
 * - Project: Accessibility Resource Platform (dr.eamer.dev/accessibility)
 * - Pattern used in theme switcher and dynamic content updates
 */


// ============================================================================
// CORE ANNOUNCEMENT CLASS
// ============================================================================

class ScreenReaderAnnouncer {
  /**
   * Initialize the screen reader announcer
   *
   * @param {Object} config - Configuration options
   * @param {number} config.cleanupDelay - Ms before removing announcement (default: 1000)
   * @param {string} config.srOnlyClass - CSS class for visually hidden content
   */
  constructor(config = {}) {
    this.cleanupDelay = config.cleanupDelay || 1000;
    this.srOnlyClass = config.srOnlyClass || 'sr-only';
    this.announcementQueue = [];
    this.isProcessing = false;
  }

  /**
   * Announce a message to screen readers
   *
   * @param {string} message - Message to announce
   * @param {string} priority - 'polite' (default) or 'assertive'
   * @param {boolean} atomic - Whether to read as atomic unit (default: true)
   */
  announce(message, priority = 'polite', atomic = true) {
    const announcement = document.createElement('div');

    // Set ARIA attributes
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', priority);
    announcement.setAttribute('aria-atomic', atomic.toString());

    // Visually hide but keep accessible to screen readers
    announcement.className = this.srOnlyClass;

    // Set the message
    announcement.textContent = message;

    // Add to DOM
    document.body.appendChild(announcement);

    // Clean up after delay
    setTimeout(() => {
      if (announcement.parentNode) {
        announcement.remove();
      }
    }, this.cleanupDelay);

    return announcement;
  }

  /**
   * Announce with 'assertive' priority (interrupts current speech)
   * Use for urgent messages like errors
   *
   * @param {string} message - Message to announce
   */
  announceAssertive(message) {
    return this.announce(message, 'assertive');
  }

  /**
   * Announce with 'polite' priority (waits for pause)
   * Use for non-urgent updates
   *
   * @param {string} message - Message to announce
   */
  announcePolite(message) {
    return this.announce(message, 'polite');
  }

  /**
   * Announce after a delay
   * Useful when you need to wait for DOM updates to complete
   *
   * @param {string} message - Message to announce
   * @param {number} delay - Delay in milliseconds
   * @param {string} priority - 'polite' or 'assertive'
   */
  announceDelayed(message, delay = 100, priority = 'polite') {
    setTimeout(() => {
      this.announce(message, priority);
    }, delay);
  }

  /**
   * Create a persistent live region for repeated announcements
   * More efficient than creating/destroying regions for frequent updates
   *
   * @param {string} id - Unique ID for the region
   * @param {string} priority - 'polite' or 'assertive'
   * @returns {HTMLElement} The live region element
   */
  createLiveRegion(id, priority = 'polite') {
    // Check if region already exists
    let region = document.getElementById(id);

    if (!region) {
      region = document.createElement('div');
      region.id = id;
      region.setAttribute('role', 'status');
      region.setAttribute('aria-live', priority);
      region.setAttribute('aria-atomic', 'true');
      region.className = this.srOnlyClass;
      document.body.appendChild(region);
    }

    return region;
  }

  /**
   * Update a persistent live region with new content
   *
   * @param {string} id - Region ID
   * @param {string} message - New message
   */
  updateLiveRegion(id, message) {
    const region = document.getElementById(id);
    if (region) {
      region.textContent = message;
    }
  }

  /**
   * Remove a persistent live region
   *
   * @param {string} id - Region ID
   */
  removeLiveRegion(id) {
    const region = document.getElementById(id);
    if (region) {
      region.remove();
    }
  }
}


// ============================================================================
// STANDALONE HELPER FUNCTIONS
// ============================================================================

/**
 * Simple announce function (no class required)
 * Good for quick integration
 *
 * @param {string} message - Message to announce
 * @param {string} priority - 'polite' or 'assertive'
 */
function announceToScreenReader(message, priority = 'polite') {
  const announcement = document.createElement('div');
  announcement.setAttribute('role', 'status');
  announcement.setAttribute('aria-live', priority);
  announcement.className = 'sr-only';
  announcement.textContent = message;

  document.body.appendChild(announcement);

  setTimeout(() => announcement.remove(), 1000);
}


/**
 * Announce form validation errors
 *
 * @param {string} fieldName - Name of the field with error
 * @param {string} errorMessage - Error description
 */
function announceFormError(fieldName, errorMessage) {
  announceToScreenReader(
    `Error in ${fieldName}: ${errorMessage}`,
    'assertive'
  );
}


/**
 * Announce successful operation
 *
 * @param {string} message - Success message
 */
function announceSuccess(message) {
  announceToScreenReader(`Success: ${message}`, 'polite');
}


/**
 * Announce loading state
 *
 * @param {boolean} isLoading - Whether content is loading
 * @param {string} context - What is loading (optional)
 */
function announceLoading(isLoading, context = 'content') {
  const message = isLoading
    ? `Loading ${context}, please wait`
    : `${context} loaded`;

  announceToScreenReader(message, 'polite');
}


// ============================================================================
// SPECIALIZED ANNOUNCEMENT PATTERNS
// ============================================================================

/**
 * Announce page navigation in SPAs
 *
 * @param {string} pageName - Name of the new page/view
 */
function announcePageChange(pageName) {
  announceToScreenReader(`Navigated to ${pageName}`, 'assertive');
}


/**
 * Announce search results count
 *
 * @param {number} count - Number of results
 * @param {string} query - Search query
 */
function announceSearchResults(count, query) {
  const message = count === 0
    ? `No results found for "${query}"`
    : count === 1
    ? `1 result found for "${query}"`
    : `${count} results found for "${query}"`;

  announceToScreenReader(message, 'polite');
}


/**
 * Announce filter updates
 *
 * @param {number} visibleCount - Number of visible items after filter
 * @param {number} totalCount - Total number of items
 */
function announceFilterUpdate(visibleCount, totalCount) {
  announceToScreenReader(
    `Showing ${visibleCount} of ${totalCount} items`,
    'polite'
  );
}


/**
 * Announce modal dialog state
 *
 * @param {boolean} isOpen - Whether modal is opening or closing
 * @param {string} modalTitle - Title of the modal
 */
function announceModal(isOpen, modalTitle) {
  const message = isOpen
    ? `${modalTitle} dialog opened`
    : `${modalTitle} dialog closed`;

  announceToScreenReader(message, 'assertive');
}


// ============================================================================
// CSS REQUIRED FOR SCREEN-READER-ONLY CONTENT
// ============================================================================

/**
 * Add this CSS to your stylesheet:
 *
 * .sr-only {
 *   position: absolute;
 *   width: 1px;
 *   height: 1px;
 *   padding: 0;
 *   margin: -1px;
 *   overflow: hidden;
 *   clip: rect(0, 0, 0, 0);
 *   white-space: nowrap;
 *   border: 0;
 * }
 *
 * This class visually hides content while keeping it accessible to
 * screen readers. Never use display:none or visibility:hidden for
 * announcement regions as they hide content from screen readers too.
 */


// ============================================================================
// USAGE EXAMPLES
// ============================================================================

// Example 1: Basic announcement
document.getElementById('submit-button').addEventListener('click', () => {
  announceToScreenReader('Form submitted successfully', 'polite');
});

// Example 2: Using the class
const announcer = new ScreenReaderAnnouncer();

document.getElementById('load-data').addEventListener('click', async () => {
  announcer.announce('Loading data, please wait', 'polite');

  try {
    const data = await fetchData();
    announcer.announce('Data loaded successfully', 'polite');
  } catch (error) {
    announcer.announceAssertive('Error loading data');
  }
});

// Example 3: Form validation
document.getElementById('email').addEventListener('blur', (e) => {
  const email = e.target.value;
  if (!email.includes('@')) {
    announceFormError('Email', 'Please enter a valid email address');
  }
});

// Example 4: Search results
function handleSearchResults(results, query) {
  announceSearchResults(results.length, query);
}

// Example 5: Persistent live region for real-time updates
const announcer2 = new ScreenReaderAnnouncer();
const chatRegion = announcer2.createLiveRegion('chat-announcements', 'polite');

function onNewChatMessage(username, message) {
  announcer2.updateLiveRegion(
    'chat-announcements',
    `New message from ${username}: ${message}`
  );
}

// Example 6: Filter updates
document.getElementById('category-filter').addEventListener('change', () => {
  const visibleItems = document.querySelectorAll('.item:not(.hidden)').length;
  const totalItems = document.querySelectorAll('.item').length;
  announceFilterUpdate(visibleItems, totalItems);
});

// Example 7: Theme switcher integration
document.querySelectorAll('.theme-button').forEach(button => {
  button.addEventListener('click', () => {
    const themeName = button.dataset.themeName;
    announceToScreenReader(`Theme changed to ${themeName}`, 'polite');
  });
});

// Example 8: Modal dialog
function openModal(modalTitle) {
  announceModal(true, modalTitle);
  // ... rest of modal opening logic
}

function closeModal(modalTitle) {
  announceModal(false, modalTitle);
  // ... rest of modal closing logic
}

// Example 9: Delayed announcement after DOM update
function addListItem(text) {
  const list = document.getElementById('dynamic-list');
  const item = document.createElement('li');
  item.textContent = text;
  list.appendChild(item);

  // Wait for DOM to update before announcing
  announcer.announceDelayed(`Added ${text} to list`, 100);
}

// Example 10: Integration with React/Vue
// React example:
/*
function MyComponent() {
  const [announcer] = useState(() => new ScreenReaderAnnouncer());

  const handleAction = () => {
    announcer.announce('Action completed');
  };

  return <button onClick={handleAction}>Do Something</button>;
}
*/


// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    ScreenReaderAnnouncer,
    announceToScreenReader,
    announceFormError,
    announceSuccess,
    announceLoading,
    announcePageChange,
    announceSearchResults,
    announceFilterUpdate,
    announceModal
  };
}
