---
name: mobile-uiux
description: Mobile UI/UX design and development for React Native / Expo apps. Use when creating, improving, or reviewing mobile app interfaces, component design, navigation patterns, design systems, or user experience flows. Covers iOS/Android design guidelines, component libraries, animations, accessibility, and mobile-specific UX patterns.
---

# Mobile UI/UX

## Overview

This skill provides guidelines and resources for designing and building high-quality mobile interfaces with React Native / Expo. It covers platform conventions (iOS/Android), reusable component patterns, navigation structures, and UX best practices.

## Quick Start

1. **New app?** Start with [expo-boilerplate](assets/expo-boilerplate/)
2. **Design system needed?** See [references/design-system.md](references/design-system.md)
3. **Component patterns?** Check [references/components.md](references/components.md)
4. **Navigation?** See [references/navigation.md](references/navigation.md)

## Platform Guidelines

### iOS (Human Interface Guidelines)
- **Navigation**: Tab bars (bottom), navigation bars (top), modal presentations
- **Typography**: San Francisco font family, dynamic type support
- **Touch targets**: Minimum 44x44 points
- **Safe areas**: Respect notches, home indicators, status bars

### Android (Material Design 3)
- **Navigation**: Bottom navigation, navigation drawer, app bars
- **Typography**: Roboto / system fonts
- **Touch targets**: Minimum 48x48 dp
- **Elevation**: Shadows, surface layers, depth hierarchy

### Cross-Platform Rules
- Use `Platform.select()` or `Platform.OS` for platform-specific code
- Respect safe areas with `react-native-safe-area-context`
- Test on both platforms — visual parity ≠ identical UI

## Core Principles

### Mobile-First Design
- Content hierarchy: Most important info first
- Thumb zones: Place primary actions in bottom 25% of screen
- Progressive disclosure: Hide complexity behind taps/swipes
- One-handed use: Design for single-thumb operation

### Performance Matters
- 60fps animations or don't animate
- List virtualization for long scrolls
- Image optimization and lazy loading
- Reduce re-renders, memoize when needed

## Resources

### references/

- **design-system.md** — Colors, typography, spacing, shadows tokens
- **components.md** — Button, card, input, list, modal patterns
- **navigation.md** — Stack, tab, drawer patterns with code
- **animations.md** — Reanimated examples, gesture handling
- **accessibility.md** — Screen reader, contrast, focus management
- **images.md** — Responsive images, caching, optimization

### assets/

- **expo-boilerplate/** — Ready-to-use Expo project structure
- **component-templates/** — Common component starter files

### scripts/

- `generate-iconset.py` — Generate iOS/Android icon sets from source
- `extract-colors.py` — Extract color palette from image
