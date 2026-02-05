/**
 * Accessible Theme Switcher Pattern
 *
 * Description: Comprehensive theme switching implementation with accessibility features
 * including screen reader announcements, keyboard navigation, localStorage persistence,
 * and ARIA attributes for proper state communication.
 *
 * Use Cases:
 * - Accessibility-first websites requiring multiple contrast/color modes
 * - Applications for users with visual impairments (CVI, photophobia, colorblindness)
 * - Dark/light mode implementations
 * - High contrast mode support
 * - User preference persistence across sessions
 *
 * Dependencies:
 * - Modern browser with localStorage support
 * - CSS custom properties (CSS variables)
 * - ARIA attribute support
 *
 * Notes:
 * - Themes are implemented using CSS custom properties (CSS variables)
 * - Changes are announced to screen readers via aria-live regions
 * - Theme preference persists in localStorage
 * - Buttons use aria-pressed for state indication
 * - Supports multiple theme presets (dark, light, high contrast, CVI-optimized, etc.)
 * - Falls back gracefully if localStorage unavailable
 *
 * Related Snippets:
 * - accessibility/screen_reader_announcements.js - Announcement patterns
 * - accessibility/keyboard_navigation_pattern.js - Keyboard support
 * - utilities/local_storage_manager.js - Storage patterns
 *
 * Source Attribution:
 * - Extracted from: /home/coolhand/html/accessibility/index.html
 * - Author: Luke Steuber
 * - Project: Accessibility Resource Platform (dr.eamer.dev/accessibility)
 * - Features support for CVI (Cortical Visual Impairment), photophobia, and color blindness
 */


// ============================================================================
// CORE THEME SWITCHER CLASS
// ============================================================================

class AccessibleThemeSwitcher {
  /**
   * Initialize the theme switcher with default configuration
   *
   * @param {Object} config - Configuration options
   * @param {string} config.storageKey - localStorage key for persistence
   * @param {string} config.defaultTheme - Default theme name
   * @param {string} config.buttonSelector - CSS selector for theme buttons
   * @param {string} config.targetElement - Element to apply theme to (default: html)
   */
  constructor(config = {}) {
    this.storageKey = config.storageKey || 'accessibilityTheme';
    this.defaultTheme = config.defaultTheme || 'dark';
    this.buttonSelector = config.buttonSelector || '.theme-button';
    this.targetElement = config.targetElement || document.documentElement;
    this.themeButtons = document.querySelectorAll(this.buttonSelector);

    this.init();
  }

  /**
   * Initialize theme system: load saved theme and set up event listeners
   */
  init() {
    this.loadTheme();
    this.attachEventListeners();
  }

  /**
   * Load saved theme from localStorage or use default
   */
  loadTheme() {
    const savedTheme = this.getSavedTheme() || this.defaultTheme;
    this.setTheme(savedTheme, false); // false = don't announce on initial load
  }

  /**
   * Get saved theme from localStorage
   *
   * @returns {string|null} Saved theme name or null
   */
  getSavedTheme() {
    try {
      return localStorage.getItem(this.storageKey);
    } catch (e) {
      console.warn('localStorage not available:', e);
      return null;
    }
  }

  /**
   * Save theme to localStorage
   *
   * @param {string} theme - Theme name to save
   */
  saveTheme(theme) {
    try {
      localStorage.setItem(this.storageKey, theme);
    } catch (e) {
      console.warn('Could not save theme to localStorage:', e);
    }
  }

  /**
   * Set the active theme
   *
   * @param {string} theme - Theme name
   * @param {boolean} announce - Whether to announce to screen readers
   */
  setTheme(theme, announce = true) {
    // Remove all theme attributes
    this.targetElement.removeAttribute('data-theme');

    // Set new theme (only if not default)
    if (theme !== this.defaultTheme) {
      this.targetElement.setAttribute('data-theme', theme);
    }

    // Update button states
    this.updateButtonStates(theme);

    // Save to localStorage
    this.saveTheme(theme);

    // Announce to screen readers
    if (announce) {
      const themeName = this.getThemeDisplayName(theme);
      this.announceToScreenReader(`Theme changed to ${themeName}`);
    }
  }

  /**
   * Update aria-pressed state on all theme buttons
   *
   * @param {string} activeTheme - Currently active theme
   */
  updateButtonStates(activeTheme) {
    this.themeButtons.forEach(button => {
      const buttonTheme = button.dataset.theme;
      const isActive = buttonTheme === activeTheme;

      button.classList.toggle('active', isActive);
      button.setAttribute('aria-pressed', isActive.toString());
    });
  }

  /**
   * Get human-readable display name for theme
   *
   * @param {string} theme - Theme identifier
   * @returns {string} Display name
   */
  getThemeDisplayName(theme) {
    const button = document.querySelector(`[data-theme="${theme}"] strong`);
    return button ? button.textContent : theme;
  }

  /**
   * Announce message to screen readers using aria-live region
   *
   * @param {string} message - Message to announce
   */
  announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.className = 'sr-only';
    announcement.textContent = message;

    document.body.appendChild(announcement);

    // Remove after screen reader has time to announce
    setTimeout(() => announcement.remove(), 1000);
  }

  /**
   * Attach click event listeners to theme buttons
   */
  attachEventListeners() {
    this.themeButtons.forEach(button => {
      button.addEventListener('click', () => {
        const theme = button.dataset.theme;
        this.setTheme(theme);
      });
    });
  }

  /**
   * Get current active theme
   *
   * @returns {string} Current theme name
   */
  getCurrentTheme() {
    const currentDataTheme = this.targetElement.getAttribute('data-theme');
    return currentDataTheme || this.defaultTheme;
  }
}


// ============================================================================
// STANDALONE IMPLEMENTATION (WITHOUT CLASS)
// ============================================================================

/**
 * Simple theme switcher implementation without using classes
 * Good for quick integration into existing projects
 */
function initSimpleThemeSwitcher() {
  const themeButtons = document.querySelectorAll('.theme-button');
  const htmlElement = document.documentElement;
  const STORAGE_KEY = 'accessibilityTheme';
  const DEFAULT_THEME = 'dark';

  // Load saved theme or use default
  function loadTheme() {
    const savedTheme = localStorage.getItem(STORAGE_KEY) || DEFAULT_THEME;
    setTheme(savedTheme, false);
  }

  // Set theme and update UI
  function setTheme(theme, announce = true) {
    // Remove all theme attributes
    htmlElement.removeAttribute('data-theme');

    // Set new theme (only if not default)
    if (theme !== DEFAULT_THEME) {
      htmlElement.setAttribute('data-theme', theme);
    }

    // Update buttons
    themeButtons.forEach(button => {
      const isActive = button.dataset.theme === theme;
      button.classList.toggle('active', isActive);
      button.setAttribute('aria-pressed', isActive.toString());
    });

    // Save to localStorage
    localStorage.setItem(STORAGE_KEY, theme);

    // Announce to screen readers
    if (announce) {
      const themeName = document.querySelector(`[data-theme="${theme}"] strong`).textContent;
      announceToScreenReader(`Theme changed to ${themeName}`);
    }
  }

  // Screen reader announcement
  function announceToScreenReader(message) {
    const announcement = document.createElement('div');
    announcement.setAttribute('role', 'status');
    announcement.setAttribute('aria-live', 'polite');
    announcement.className = 'sr-only';
    announcement.textContent = message;
    document.body.appendChild(announcement);
    setTimeout(() => announcement.remove(), 1000);
  }

  // Add click handlers
  themeButtons.forEach(button => {
    button.addEventListener('click', () => {
      setTheme(button.dataset.theme);
    });
  });

  // Initialize
  loadTheme();
}


// ============================================================================
// HTML STRUCTURE EXAMPLE
// ============================================================================

/**
 * Required HTML structure:
 *
 * <div class="theme-switcher" role="group" aria-label="Theme selection">
 *   <button class="theme-button" data-theme="dark" aria-pressed="false">
 *     <strong>High Contrast Dark</strong>
 *     <span>Default theme with excellent contrast</span>
 *   </button>
 *
 *   <button class="theme-button" data-theme="light" aria-pressed="false">
 *     <strong>High Contrast Light</strong>
 *     <span>Light background with dark text</span>
 *   </button>
 *
 *   <button class="theme-button" data-theme="cvi" aria-pressed="false">
 *     <strong>CVI-Optimized</strong>
 *     <span>Yellow on black for cortical visual impairment</span>
 *   </button>
 * </div>
 *
 * CSS for screen reader only content:
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
 */


// ============================================================================
// CSS CUSTOM PROPERTIES EXAMPLE
// ============================================================================

/**
 * Define themes using CSS custom properties:
 *
 * :root {
 *   --bg: #000000;
 *   --text: #ffffff;
 *   --accent: #00d4ff;
 *   --focus-ring: #ffff00;
 * }
 *
 * [data-theme="light"] {
 *   --bg: #ffffff;
 *   --text: #000000;
 *   --accent: #0000ff;
 *   --focus-ring: #ff00ff;
 * }
 *
 * [data-theme="cvi"] {
 *   --bg: #000000;
 *   --text: #ffff00;
 *   --accent: #ffff00;
 *   --focus-ring: #00ffff;
 * }
 *
 * body {
 *   background: var(--bg);
 *   color: var(--text);
 * }
 *
 * a {
 *   color: var(--accent);
 * }
 *
 * *:focus {
 *   outline: 3px solid var(--focus-ring);
 * }
 */


// ============================================================================
// USAGE EXAMPLES
// ============================================================================

// Example 1: Using the class
document.addEventListener('DOMContentLoaded', () => {
  const themeSwitcher = new AccessibleThemeSwitcher({
    storageKey: 'myAppTheme',
    defaultTheme: 'dark',
    buttonSelector: '.theme-button'
  });

  // Programmatically change theme
  // themeSwitcher.setTheme('light');

  // Get current theme
  // const current = themeSwitcher.getCurrentTheme();
});

// Example 2: Using the simple function
// document.addEventListener('DOMContentLoaded', initSimpleThemeSwitcher);

// Example 3: Respect user's OS preference
document.addEventListener('DOMContentLoaded', () => {
  // Check for saved preference first, then OS preference
  const savedTheme = localStorage.getItem('accessibilityTheme');

  if (!savedTheme) {
    // User hasn't set a preference, check OS
    const prefersDark = window.matchMedia('(prefers-color-scheme: dark)').matches;
    const defaultTheme = prefersDark ? 'dark' : 'light';

    const themeSwitcher = new AccessibleThemeSwitcher({
      defaultTheme: defaultTheme
    });
  } else {
    const themeSwitcher = new AccessibleThemeSwitcher();
  }
});

// Example 4: Listen for OS preference changes
const darkModeQuery = window.matchMedia('(prefers-color-scheme: dark)');
darkModeQuery.addEventListener('change', (e) => {
  // Only auto-switch if user hasn't set a manual preference
  if (!localStorage.getItem('accessibilityTheme')) {
    const theme = e.matches ? 'dark' : 'light';
    // Update theme...
  }
});


// Export for use in modules
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { AccessibleThemeSwitcher, initSimpleThemeSwitcher };
}
