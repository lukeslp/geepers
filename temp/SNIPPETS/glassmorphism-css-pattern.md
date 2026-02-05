# Glassmorphism CSS Design Pattern

**Source**: `/home/coolhand/html/datavis/language-tree/css/style.css`
**Date**: 2025-12-15
**Use Case**: Modern UI with frosted glass effect, dark theme, neon accents

## Core CSS Custom Properties

```css
:root {
    /* Background Layers */
    --bg-primary: #0a0a0a;          /* Deep black base */
    --bg-secondary: #111111;         /* Slightly lighter */
    --bg-tertiary: #1a1a1a;          /* Card backgrounds */
    --bg-panel: rgba(0, 0, 0, 0.85); /* Semi-transparent panels */
    --bg-glass: rgba(15, 15, 15, 0.9); /* Glassmorphism effect */

    /* Text Hierarchy */
    --text-primary: #ffffff;
    --text-secondary: #cccccc;
    --text-muted: #888888;
    --text-dim: #444444;

    /* Neon Color Palette */
    --color-accent: #18FFFF;         /* Cyan glow */
    --color-indo-european: #18FFFF;
    --color-sino-tibetan: #FF6E40;
    --color-afroasiatic: #FFD740;
    --color-niger-congo: #FF4081;
    --color-dravidian: #EA80FC;
    /* ... more family colors */

    /* Spacing Scale (8px base) */
    --space-xs: 4px;
    --space-sm: 8px;
    --space-md: 16px;
    --space-lg: 24px;
    --space-xl: 32px;
    --space-2xl: 48px;

    /* Typography */
    --font-display: 'Playfair Display', Georgia, serif;
    --font-mono: 'Space Mono', 'Courier New', monospace;
    --font-sans: system-ui, -apple-system, sans-serif;

    /* Glow Effects */
    --glow-sm: 0 0 5px currentColor;
    --glow-md: 0 0 10px currentColor, 0 0 20px currentColor;
    --glow-lg: 0 0 15px currentColor, 0 0 30px currentColor, 0 0 45px currentColor;

    /* Transitions */
    --transition-fast: 150ms ease;
    --transition-normal: 300ms ease;
    --transition-slow: 500ms ease;

    /* Z-Index Layers */
    --z-base: 1;
    --z-header: 50;
    --z-panel: 60;
    --z-modal: 70;
    --z-loading: 100;
}
```

## Glassmorphism Card Component

```css
.glass-card {
    background: var(--bg-glass);
    backdrop-filter: blur(20px) saturate(150%);
    -webkit-backdrop-filter: blur(20px) saturate(150%);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 12px;
    padding: var(--space-lg);
    box-shadow:
        0 8px 32px rgba(0, 0, 0, 0.3),
        inset 0 1px 0 rgba(255, 255, 255, 0.05);
    transition: all var(--transition-normal);
}

.glass-card:hover {
    border-color: rgba(255, 255, 255, 0.2);
    box-shadow:
        0 12px 48px rgba(0, 0, 0, 0.4),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    transform: translateY(-2px);
}

/* Semi-transparent variant */
.glass-panel {
    background: rgba(0, 0, 0, 0.6);
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255, 255, 255, 0.05);
}
```

## Neon Glow Text Effect

```css
.glow-text {
    color: var(--color-accent);
    text-shadow: var(--glow-md);
    font-family: var(--font-display);
    font-weight: 700;
    letter-spacing: 0.05em;
}

/* Animated pulsing glow */
@keyframes glow-pulse {
    0%, 100% {
        text-shadow: var(--glow-md);
        opacity: 1;
    }
    50% {
        text-shadow: var(--glow-lg);
        opacity: 0.9;
    }
}

.glow-text-animated {
    animation: glow-pulse 3s ease-in-out infinite;
}

/* Subtle glow on hover */
.glow-hover {
    transition: text-shadow var(--transition-normal);
}

.glow-hover:hover {
    text-shadow: var(--glow-lg);
}
```

## Tab Navigation with Glassmorphism

```css
.tab-navigation {
    display: flex;
    gap: var(--space-sm);
    background: rgba(0, 0, 0, 0.4);
    backdrop-filter: blur(10px);
    border-radius: 20px;
    padding: var(--space-xs);
    border: 1px solid rgba(255, 255, 255, 0.05);
}

.tab-button {
    display: flex;
    align-items: center;
    gap: var(--space-sm);
    padding: var(--space-sm) var(--space-lg);
    background: transparent;
    border: 1px solid transparent;
    border-radius: 16px;
    color: var(--text-muted);
    font-family: var(--font-mono);
    font-size: 14px;
    cursor: pointer;
    transition: all var(--transition-normal);
    position: relative;
}

.tab-button:hover {
    color: var(--text-secondary);
    background: rgba(255, 255, 255, 0.03);
}

.tab-button.active {
    color: var(--color-accent);
    background: rgba(24, 255, 255, 0.1);
    border-color: rgba(24, 255, 255, 0.3);
    text-shadow: var(--glow-sm);
}

.tab-button.active::before {
    content: '';
    position: absolute;
    inset: -1px;
    border-radius: 16px;
    padding: 1px;
    background: linear-gradient(135deg,
        rgba(24, 255, 255, 0.4),
        rgba(24, 255, 255, 0.1));
    -webkit-mask:
        linear-gradient(#fff 0 0) content-box,
        linear-gradient(#fff 0 0);
    -webkit-mask-composite: xor;
    mask-composite: exclude;
}
```

## Overlay Panel with Blur

```css
.info-panel {
    position: fixed;
    top: 80px;
    right: var(--space-lg);
    width: 320px;
    max-height: calc(100vh - 120px);
    overflow-y: auto;
    background: var(--bg-glass);
    backdrop-filter: blur(20px);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 16px;
    padding: var(--space-lg);
    box-shadow:
        0 20px 60px rgba(0, 0, 0, 0.5),
        inset 0 1px 0 rgba(255, 255, 255, 0.1);
    z-index: var(--z-panel);
    transform: translateX(calc(100% + var(--space-lg)));
    transition: transform var(--transition-normal);
}

.info-panel.visible {
    transform: translateX(0);
}

/* Custom scrollbar for dark theme */
.info-panel::-webkit-scrollbar {
    width: 8px;
}

.info-panel::-webkit-scrollbar-track {
    background: rgba(255, 255, 255, 0.05);
    border-radius: 4px;
}

.info-panel::-webkit-scrollbar-thumb {
    background: rgba(255, 255, 255, 0.2);
    border-radius: 4px;
}

.info-panel::-webkit-scrollbar-thumb:hover {
    background: rgba(255, 255, 255, 0.3);
}
```

## Button Variants

```css
/* Primary button with glow */
.btn-primary {
    padding: var(--space-sm) var(--space-lg);
    background: var(--color-accent);
    color: var(--bg-primary);
    border: none;
    border-radius: 8px;
    font-family: var(--font-mono);
    font-weight: 700;
    font-size: 14px;
    cursor: pointer;
    box-shadow: 0 0 20px rgba(24, 255, 255, 0.3);
    transition: all var(--transition-normal);
}

.btn-primary:hover {
    box-shadow: 0 0 30px rgba(24, 255, 255, 0.5);
    transform: translateY(-2px);
}

/* Ghost button with border glow */
.btn-ghost {
    padding: var(--space-sm) var(--space-lg);
    background: transparent;
    color: var(--color-accent);
    border: 1px solid rgba(24, 255, 255, 0.3);
    border-radius: 8px;
    font-family: var(--font-mono);
    font-size: 14px;
    cursor: pointer;
    transition: all var(--transition-normal);
}

.btn-ghost:hover {
    background: rgba(24, 255, 255, 0.1);
    border-color: rgba(24, 255, 255, 0.5);
    box-shadow: 0 0 15px rgba(24, 255, 255, 0.2);
}
```

## Input Fields with Glass Effect

```css
.input-glass {
    width: 100%;
    padding: var(--space-sm) var(--space-md);
    background: rgba(255, 255, 255, 0.03);
    border: 1px solid rgba(255, 255, 255, 0.1);
    border-radius: 8px;
    color: var(--text-primary);
    font-family: var(--font-mono);
    font-size: 14px;
    backdrop-filter: blur(10px);
    transition: all var(--transition-normal);
}

.input-glass::placeholder {
    color: var(--text-muted);
}

.input-glass:focus {
    outline: none;
    border-color: rgba(24, 255, 255, 0.5);
    background: rgba(255, 255, 255, 0.05);
    box-shadow: 0 0 20px rgba(24, 255, 255, 0.2);
}
```

## Responsive Breakpoints

```css
/* Mobile-first approach */
@media (max-width: 768px) {
    .glass-card {
        padding: var(--space-md);
        border-radius: 8px;
    }

    .info-panel {
        width: calc(100% - 2 * var(--space-md));
        right: var(--space-md);
    }

    .tab-button {
        padding: var(--space-xs) var(--space-sm);
        font-size: 12px;
    }
}

@media (max-width: 480px) {
    .glass-card {
        backdrop-filter: blur(10px); /* Reduce blur for performance */
    }

    .tab-navigation {
        flex-direction: column;
    }
}
```

## Key Features

1. **Layered Backgrounds**: Multiple transparency levels for depth
2. **Backdrop Blur**: Modern frosted glass effect (requires vendor prefixes)
3. **Neon Accents**: Color-coded glow effects for visual hierarchy
4. **Smooth Transitions**: 300ms easing for professional feel
5. **Z-Index System**: Predictable layering with CSS variables
6. **Responsive**: Mobile-first with performance optimizations

## Browser Compatibility

- **backdrop-filter**: Chrome 76+, Safari 9+, Firefox 103+
- Use `-webkit-backdrop-filter` for Safari
- Provide fallback backgrounds for older browsers
- Test on mobile devices (can impact performance)

## Performance Tips

- Limit blur radius on mobile (<10px)
- Use `will-change` sparingly for animations
- Minimize overlapping blur layers
- Consider `contain: layout style paint` for isolated components

## Related Patterns

- See `d3-radial-tree-pattern.md` for SVG glow filters
- See `es6-lazy-loading-pattern.md` for module organization
