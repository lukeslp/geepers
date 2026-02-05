/**
 * Keyboard Navigation Patterns
 *
 * Description: Comprehensive patterns for implementing keyboard navigation,
 * including smooth scrolling with offset, focus management, and WCAG-compliant
 * keyboard interaction patterns for custom widgets.
 *
 * Use Cases:
 * - Smooth scroll to anchor links with sticky header compensation
 * - Table of contents navigation
 * - Single page applications
 * - Custom widgets (tabs, accordions, menus)
 * - Focus trap for modals
 * - Keyboard shortcuts
 * - Roving tabindex for complex components
 *
 * Dependencies:
 * - Modern browser with DOM support
 * - Optional: ARIA attributes for custom widgets
 *
 * Notes:
 * - Follows WCAG 2.1 keyboard accessibility guidelines
 * - Implements ARIA Authoring Practices patterns
 * - Smooth scroll with offset for fixed headers
 * - Focus management for screen readers
 * - Prevents default scroll jump behavior
 * - Works with history API for proper URLs
 *
 * WCAG Requirements:
 * - 2.1.1 Keyboard (Level A): All functionality via keyboard
 * - 2.1.2 No Keyboard Trap (Level A): Focus can move away
 * - 2.4.7 Focus Visible (Level AA): Visible focus indicator
 * - 2.4.3 Focus Order (Level A): Logical focus order
 *
 * Related Snippets:
 * - accessibility/skip_links_and_landmarks.html - Skip navigation
 * - accessibility/focus_trap_pattern.js - Modal focus management
 * - accessibility/screen_reader_announcements.js - ARIA announcements
 *
 * Source Attribution:
 * - Extracted from: /home/coolhand/html/accessibility/index.html
 * - Author: Luke Steuber
 * - Project: Accessibility Resource Platform (dr.eamer.dev/accessibility)
 */


// ============================================================================
// SMOOTH SCROLL WITH OFFSET (FOR STICKY HEADERS)
// ============================================================================

/**
 * Implement smooth scrolling for anchor links with offset compensation
 * Perfect for pages with sticky/fixed headers
 *
 * @param {number} offset - Pixels to offset from top (e.g., header height)
 * @param {string} selector - CSS selector for anchor links (default: 'a[href^="#"]')
 */
function initSmoothScrollWithOffset(offset = 120, selector = 'a[href^="#"]') {
  document.querySelectorAll(selector).forEach(anchor => {
    anchor.addEventListener('click', function(e) {
      const href = this.getAttribute('href');

      // Skip special cases
      if (href === '#' || href === '#main-content') {
        return;
      }

      e.preventDefault();

      const target = document.querySelector(href);

      if (target) {
        // Calculate position with offset
        const targetPosition = target.offsetTop - offset;

        // Smooth scroll to position
        window.scrollTo({
          top: targetPosition,
          behavior: 'smooth'
        });

        // Set focus for screen reader users
        // This is critical for accessibility
        target.setAttribute('tabindex', '-1');
        target.focus();

        // Update URL without jumping
        history.pushState(null, '', href);
      }
    });
  });
}


// ============================================================================
// BACK TO TOP BUTTON
// ============================================================================

/**
 * Create accessible "Back to Top" button
 * Shows after scrolling down, scrolls smoothly to top
 */
class BackToTopButton {
  constructor(config = {}) {
    this.threshold = config.threshold || 500; // Show after scrolling this many pixels
    this.buttonId = config.buttonId || 'backToTop';
    this.button = document.getElementById(this.buttonId);

    if (this.button) {
      this.init();
    }
  }

  init() {
    // Scroll event listener (with passive for performance)
    window.addEventListener('scroll', () => {
      if (window.scrollY > this.threshold) {
        this.button.hidden = false;
      } else {
        this.button.hidden = true;
      }
    }, { passive: true });

    // Click handler
    this.button.addEventListener('click', () => {
      window.scrollTo({
        top: 0,
        behavior: 'smooth'
      });

      // Focus on first heading after scroll completes
      setTimeout(() => {
        const firstHeading = document.querySelector('h1');
        if (firstHeading) {
          firstHeading.setAttribute('tabindex', '-1');
          firstHeading.focus();
        }
      }, 500);
    });
  }
}


// ============================================================================
// KEYBOARD SHORTCUT MANAGER
// ============================================================================

/**
 * Manage keyboard shortcuts accessibly
 * Supports Ctrl/Cmd modifiers and prevents conflicts
 */
class KeyboardShortcutManager {
  constructor() {
    this.shortcuts = new Map();
    this.init();
  }

  init() {
    document.addEventListener('keydown', (e) => {
      const key = this.getKeyCombo(e);
      const handler = this.shortcuts.get(key);

      if (handler) {
        // Don't interfere with form inputs
        if (this.isTypingInInput(e)) {
          return;
        }

        e.preventDefault();
        handler(e);
      }
    });
  }

  /**
   * Get normalized key combination string
   */
  getKeyCombo(e) {
    const parts = [];

    if (e.ctrlKey || e.metaKey) parts.push('ctrl');
    if (e.altKey) parts.push('alt');
    if (e.shiftKey) parts.push('shift');

    parts.push(e.key.toLowerCase());

    return parts.join('+');
  }

  /**
   * Check if user is typing in input field
   */
  isTypingInInput(e) {
    const target = e.target;
    const tagName = target.tagName.toLowerCase();

    return (
      tagName === 'input' ||
      tagName === 'textarea' ||
      target.isContentEditable
    );
  }

  /**
   * Register a keyboard shortcut
   *
   * @param {string} combo - Key combination (e.g., 'ctrl+k', 'alt+h')
   * @param {Function} handler - Function to call when shortcut pressed
   * @param {string} description - Description for help/docs
   */
  register(combo, handler, description = '') {
    this.shortcuts.set(combo.toLowerCase(), handler);

    // Store description for help display
    handler.description = description;
  }

  /**
   * Unregister a keyboard shortcut
   */
  unregister(combo) {
    this.shortcuts.delete(combo.toLowerCase());
  }

  /**
   * Get all registered shortcuts (for help display)
   */
  getAll() {
    const shortcuts = [];

    this.shortcuts.forEach((handler, combo) => {
      shortcuts.push({
        combo,
        description: handler.description || 'No description'
      });
    });

    return shortcuts;
  }
}


// ============================================================================
// ROVING TABINDEX PATTERN
// ============================================================================

/**
 * Implement roving tabindex for custom widget navigation
 * Used for toolbars, menus, tab lists, etc.
 *
 * Arrow keys navigate, Tab moves out of widget
 */
class RovingTabindex {
  constructor(container, config = {}) {
    this.container = container;
    this.items = Array.from(container.querySelectorAll(config.itemSelector || '[role="tab"], [role="menuitem"]'));
    this.currentIndex = 0;
    this.orientation = config.orientation || 'horizontal'; // 'horizontal' or 'vertical'

    this.init();
  }

  init() {
    // Set initial tabindex states
    this.items.forEach((item, index) => {
      item.setAttribute('tabindex', index === 0 ? '0' : '-1');
    });

    // Add keyboard navigation
    this.container.addEventListener('keydown', (e) => {
      this.handleKeydown(e);
    });

    // Track current focus
    this.items.forEach((item, index) => {
      item.addEventListener('focus', () => {
        this.currentIndex = index;
      });
    });
  }

  handleKeydown(e) {
    const prevKey = this.orientation === 'horizontal' ? 'ArrowLeft' : 'ArrowUp';
    const nextKey = this.orientation === 'horizontal' ? 'ArrowRight' : 'ArrowDown';

    let newIndex = this.currentIndex;

    switch (e.key) {
      case nextKey:
        e.preventDefault();
        newIndex = (this.currentIndex + 1) % this.items.length;
        break;

      case prevKey:
        e.preventDefault();
        newIndex = (this.currentIndex - 1 + this.items.length) % this.items.length;
        break;

      case 'Home':
        e.preventDefault();
        newIndex = 0;
        break;

      case 'End':
        e.preventDefault();
        newIndex = this.items.length - 1;
        break;

      default:
        return;
    }

    this.focusItem(newIndex);
  }

  focusItem(index) {
    // Update tabindex
    this.items[this.currentIndex].setAttribute('tabindex', '-1');
    this.items[index].setAttribute('tabindex', '0');

    // Move focus
    this.items[index].focus();

    // Update current index
    this.currentIndex = index;
  }
}


// ============================================================================
// ARROW KEY NAVIGATION FOR LISTS
// ============================================================================

/**
 * Add arrow key navigation to a list
 *
 * @param {HTMLElement} listElement - The list container
 * @param {string} itemSelector - Selector for focusable items
 */
function addArrowKeyNavigation(listElement, itemSelector = 'a, button') {
  const items = Array.from(listElement.querySelectorAll(itemSelector));
  let currentIndex = 0;

  listElement.addEventListener('keydown', (e) => {
    if (e.key !== 'ArrowUp' && e.key !== 'ArrowDown') {
      return;
    }

    e.preventDefault();

    // Find current focused item
    currentIndex = items.indexOf(document.activeElement);

    if (currentIndex === -1) {
      currentIndex = 0;
    }

    // Calculate new index
    if (e.key === 'ArrowDown') {
      currentIndex = (currentIndex + 1) % items.length;
    } else {
      currentIndex = (currentIndex - 1 + items.length) % items.length;
    }

    // Focus new item
    items[currentIndex].focus();
  });
}


// ============================================================================
// FOCUS TRAP FOR MODALS
// ============================================================================

/**
 * Trap focus within a modal dialog
 * Prevents Tab from leaving modal
 */
class FocusTrap {
  constructor(element) {
    this.element = element;
    this.focusableSelector = 'a[href], button:not([disabled]), textarea:not([disabled]), input:not([disabled]), select:not([disabled]), [tabindex]:not([tabindex="-1"])';
    this.previousFocus = document.activeElement;
    this.isActive = false;
  }

  activate() {
    this.isActive = true;
    this.updateFocusableElements();

    // Focus first element
    if (this.focusableElements.length > 0) {
      this.focusableElements[0].focus();
    }

    // Add event listener
    this.element.addEventListener('keydown', this.handleKeydown.bind(this));
  }

  deactivate() {
    this.isActive = false;
    this.element.removeEventListener('keydown', this.handleKeydown.bind(this));

    // Restore focus
    if (this.previousFocus && this.previousFocus.focus) {
      this.previousFocus.focus();
    }
  }

  updateFocusableElements() {
    this.focusableElements = Array.from(
      this.element.querySelectorAll(this.focusableSelector)
    );
  }

  handleKeydown(e) {
    if (e.key !== 'Tab') {
      return;
    }

    this.updateFocusableElements();

    const firstElement = this.focusableElements[0];
    const lastElement = this.focusableElements[this.focusableElements.length - 1];

    // Shift + Tab on first element -> focus last
    if (e.shiftKey && document.activeElement === firstElement) {
      e.preventDefault();
      lastElement.focus();
    }
    // Tab on last element -> focus first
    else if (!e.shiftKey && document.activeElement === lastElement) {
      e.preventDefault();
      firstElement.focus();
    }
  }
}


// ============================================================================
// USAGE EXAMPLES
// ============================================================================

// Example 1: Smooth scroll with offset for sticky header
document.addEventListener('DOMContentLoaded', () => {
  initSmoothScrollWithOffset(120); // 120px offset for header
});

// Example 2: Back to top button
const backToTop = new BackToTopButton({
  threshold: 500,
  buttonId: 'backToTop'
});

// Example 3: Keyboard shortcuts
const shortcuts = new KeyboardShortcutManager();

shortcuts.register('ctrl+k', () => {
  document.getElementById('search').focus();
}, 'Focus search');

shortcuts.register('ctrl+/', () => {
  showKeyboardShortcutsHelp();
}, 'Show keyboard shortcuts');

shortcuts.register('alt+h', () => {
  document.querySelector('h1').scrollIntoView({ behavior: 'smooth' });
}, 'Scroll to top');

// Example 4: Roving tabindex for tabs
const tabList = document.querySelector('[role="tablist"]');
if (tabList) {
  new RovingTabindex(tabList, {
    itemSelector: '[role="tab"]',
    orientation: 'horizontal'
  });
}

// Example 5: Arrow key navigation for list
const navigationList = document.getElementById('nav-list');
if (navigationList) {
  addArrowKeyNavigation(navigationList, 'a');
}

// Example 6: Focus trap for modal
function openModal() {
  const modal = document.getElementById('modal');
  const focusTrap = new FocusTrap(modal);

  modal.hidden = false;
  modal.setAttribute('aria-hidden', 'false');
  focusTrap.activate();

  // Store trap for later deactivation
  modal._focusTrap = focusTrap;
}

function closeModal() {
  const modal = document.getElementById('modal');

  if (modal._focusTrap) {
    modal._focusTrap.deactivate();
  }

  modal.hidden = true;
  modal.setAttribute('aria-hidden', 'true');
}

// Example 7: Keyboard shortcut help display
function showKeyboardShortcutsHelp() {
  const shortcuts = shortcuts.getAll();
  const helpText = shortcuts.map(s =>
    `${s.combo}: ${s.description}`
  ).join('\n');

  console.log('Keyboard Shortcuts:\n' + helpText);
  // In production, show in a modal or help panel
}


// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = {
    initSmoothScrollWithOffset,
    BackToTopButton,
    KeyboardShortcutManager,
    RovingTabindex,
    addArrowKeyNavigation,
    FocusTrap
  };
}
