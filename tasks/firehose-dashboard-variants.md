# Firehose Dashboard Variants - Task Specification

**Date**: 2026-02-14
**Project**: /home/coolhand/html/firehose
**Mode**: NewFeature
**Orchestrator**: geepers_orchestrator_frontend

## Objective

Create 4 complete React dashboard variant components for the Bluesky Firehose real-time analytics application. Each variant provides a unique visual theme and aesthetic while maintaining consistent Socket.IO integration and functionality.

## Target Location

All components go in: `/home/coolhand/html/firehose/client/src/variants/`

## Technical Context

### Technology Stack
- React 19 with TypeScript
- Tailwind CSS 4 (no CSS modules - inline Tailwind classes)
- Framer Motion 12 (for animations)
- Socket.IO client 4.8.1 (real-time updates)
- Recharts 2.15.4 (optional for charts)

### Existing Socket.IO Pattern

From `/home/coolhand/html/firehose/client/src/hooks/useSocket.ts`:

```typescript
interface FirehoseStats {
  totalPosts: number;
  postsPerMinute: number;
  sentimentCounts: {
    positive: number;
    negative: number;
    neutral: number;
  };
  duration: number;
  running: boolean;
  inDatabase?: number;
}

interface Post {
  text: string;
  sentiment: 'positive' | 'negative' | 'neutral';
  sentimentScore: number;
  createdAt: string;
  language?: string;
  hasImages?: boolean;
  hasVideo?: boolean;
  hasLink?: boolean;
  author?: {
    did: string;
    handle: string;
  };
  uri?: string;
  isReply?: boolean;
  isQuote?: boolean;
}

// Usage pattern:
const { connected, stats, latestPost } = useSocket();
```

Socket connection is established at `${import.meta.env.BASE_URL}socket.io`.

### Design System Note

The main app uses shadcn/ui components (Radix primitives). Variants can use these or build custom components - designer's choice.

## Variant Specifications

### 1. MissionControl.tsx - NASA Control Room

**Aesthetic**: NASA mission control center, 1960s-1980s space program
**Theme**: Dark background with green/amber terminal text
**Typography**: Monospace fonts (Courier New, Consolas, or similar)
**Layout**: Modular grid panels like control room monitors
**Key Features**:
- Panel-based layout (sentiment panel, rate panel, live feed panel)
- Monospace numeric displays with leading zeros
- Blinking status indicators (CSS animation)
- "Mission elapsed time" instead of duration
- Color palette: Dark gray (#1a1a1a), terminal green (#00ff00), amber (#ffbf00), red alerts (#ff0000)
- Grid layout with borders between panels

**Animation Requirements**:
- Blinking status dots for connection state
- Slide-in animations for new posts
- Odometer-style number roll for stats updates

### 2. CosmicNexus.tsx - Space/Nebula Theme

**Aesthetic**: Deep space, nebulae, cosmic vibes
**Theme**: Dark purple/blue gradient background with glowing elements
**Layout**: Posts appear as stars/particles in space
**Key Features**:
- Particle system background (CSS or Framer Motion)
- Posts rendered as glowing orbs/cards that fade in
- Sentiment color-coded glow (green=positive, red=negative, blue=neutral)
- Floating animation for post cards
- Gradient backgrounds (purple → blue → dark purple)
- Glow effects on interactive elements

**Animation Requirements**:
- Particle drift background (subtle movement)
- Posts fade in with glow effect
- Pulse animation on stats panels
- Smooth color transitions for sentiment changes

### 3. Editorial.tsx - NYT-Inspired Print

**Aesthetic**: Classic newspaper editorial design
**Theme**: White/cream background, serif typography, elegant layout
**Typography**: Serif fonts (Georgia, Garamond, or similar for body; sans-serif for stats)
**Layout**: Posts displayed as headlines in columns
**Key Features**:
- Multi-column text layout for post feed
- Posts formatted like news headlines (author as byline)
- Divider lines between sections (horizontal rules)
- Stats presented as "newspaper facts" boxes
- Color palette: Off-white (#f9f7f4), black (#000), gray (#666), red accent (#c00)
- Print-inspired borders and ornamental dividers

**Animation Requirements**:
- Typewriter effect for new post headlines (optional)
- Subtle fade-in for new content
- Minimal animations (print aesthetic)

### 4. RetroArcade.tsx - Gaming/Pixel Art

**Aesthetic**: 1980s arcade games, pixel art, CRT monitor
**Theme**: Dark background with neon colors, pixel fonts
**Typography**: Pixel/bitmap fonts (Press Start 2P if available, or similar)
**Layout**: Retro game UI with score displays
**Key Features**:
- Pixel art borders and UI elements
- Stats displayed as arcade game scores
- "HIGH SCORE" style presentation for top stats
- Scanline effect overlay (CSS)
- Color palette: Black (#000), neon green (#39ff14), cyan (#00ffff), magenta (#ff00ff), yellow (#ffff00)
- Pixelated dividers and borders

**Animation Requirements**:
- Blink/flash effect for new posts (arcade attract mode)
- Score counter increments with digit flip
- CRT scanline animation
- Glitch effects on connection state changes

## Component Structure

Each variant should follow this structure:

```typescript
// variants/MissionControl.tsx (example)

import { useSocket } from '@/hooks/useSocket';
import { motion } from 'framer-motion';
import { useState, useEffect } from 'react';

interface MissionControlProps {
  className?: string;
}

export function MissionControl({ className }: MissionControlProps) {
  const { connected, stats, latestPost } = useSocket();
  const [posts, setPosts] = useState<Post[]>([]);

  useEffect(() => {
    if (latestPost) {
      setPosts(prev => [latestPost, ...prev].slice(0, 20)); // Keep last 20
    }
  }, [latestPost]);

  // Component implementation...

  return (
    <div className={`mission-control ${className || ''}`}>
      {/* Layout implementation */}
    </div>
  );
}
```

## Acceptance Criteria

For each variant:

1. **Complete TypeScript Component**
   - Proper TypeScript types (no `any`)
   - Props interface exported
   - Handles connected/disconnected states
   - Displays stats from Socket.IO
   - Displays live posts from Socket.IO

2. **Styling**
   - All styling via Tailwind classes (no separate CSS files)
   - Responsive design (works on mobile and desktop)
   - Accessible (WCAG 2.1 AA)
   - Theme-appropriate color palette

3. **Animation**
   - Framer Motion for component animations
   - CSS animations for persistent effects (blink, scanlines, etc.)
   - Smooth transitions, no jank
   - Reduced motion support (`prefers-reduced-motion`)

4. **Socket.IO Integration**
   - Uses `useSocket()` hook correctly
   - Handles connection state
   - Updates on `stats` changes
   - Updates on `latestPost` changes

5. **Code Quality**
   - Formatted with Prettier
   - Type-checked with TypeScript
   - No console errors
   - Clean, readable code

## Files to Create

1. `/home/coolhand/html/firehose/client/src/variants/MissionControl.tsx`
2. `/home/coolhand/html/firehose/client/src/variants/CosmicNexus.tsx`
3. `/home/coolhand/html/firehose/client/src/variants/Editorial.tsx`
4. `/home/coolhand/html/firehose/client/src/variants/RetroArcade.tsx`
5. `/home/coolhand/html/firehose/client/src/variants/index.ts` (exports)

## Dependencies

All required dependencies are already in package.json:
- `react`: ^19.1.1
- `framer-motion`: ^12.23.22
- `socket.io-client`: ^4.8.1
- `tailwindcss`: ^4.1.14
- `lucide-react`: ^0.453.0 (for icons)

## Reference Implementation

See existing dashboard at `/home/coolhand/html/firehose/client/src/pages/Dashboard.tsx` for Socket.IO usage patterns.

## Success Metrics

- All 4 variants compile without TypeScript errors
- All 4 variants render correctly with live Socket.IO data
- Animations run at 60fps
- Accessibility audit passes (WCAG AA)
- Code passes `pnpm check` (TypeScript)
- Each variant has distinct visual identity
- Consistent Socket.IO integration pattern across all variants
