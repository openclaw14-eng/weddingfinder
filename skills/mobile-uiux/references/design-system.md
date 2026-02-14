# Design System

## Color Tokens

### Primary Palette
```javascript
const colors = {
  primary: {
    50: '#eff6ff',
    100: '#dbeafe',
    200: '#bfdbfe',
    300: '#93c5fd',
    400: '#60a5fa',
    500: '#3b82f6', // Main brand color
    600: '#2563eb',
    700: '#1d4ed8',
    800: '#1e40af',
    900: '#1e3a8a',
  },
  neutral: {
    0: '#ffffff',
    50: '#f9fafb',
    100: '#f3f4f6',
    200: '#e5e7eb',
    300: '#d1d5db',
    400: '#9ca3af',
    500: '#6b7280',
    600: '#4b5563',
    700: '#374151',
    800: '#1f2937',
    900: '#111827',
    950: '#030712',
  },
  semantic: {
    success: '#22c55e',
    warning: '#f59e0b',
    error: '#ef4444',
    info: '#3b82f6',
  },
};
```

### Usage Guidelines
- **Backgrounds**: neutral.0 (primary), neutral.50/100 (secondary)
- **Text**: neutral.900 (primary), neutral.600 (secondary), neutral.400 (tertiary)
- **Borders**: neutral.200
- **Disabled**: neutral.300 text on neutral.100 bg

## Typography

### Type Scale
```javascript
const typography = {
  h1: { fontSize: 32, lineHeight: 40, fontWeight: '700' },
  h2: { fontSize: 24, lineHeight: 32, fontWeight: '700' },
  h3: { fontSize: 20, lineHeight: 28, fontWeight: '600' },
  h4: { fontSize: 18, lineHeight: 24, fontWeight: '600' },
  body: { fontSize: 16, lineHeight: 24, fontWeight: '400' },
  bodySmall: { fontSize: 14, lineHeight: 20, fontWeight: '400' },
  caption: { fontSize: 12, lineHeight: 16, fontWeight: '400' },
  button: { fontSize: 16, lineHeight: 24, fontWeight: '600' },
};
```

### Font Families
```javascript
// iOS
const iosFonts = {
  regular: 'System',
  medium: 'System',
  bold: 'System',
};

// Android
const androidFonts = {
  regular: 'Roboto',
  medium: 'Roboto-Medium',
  bold: 'Roboto-Bold',
};
```

## Spacing Scale

```javascript
const spacing = {
  0: 0,
  1: 4,
  2: 8,
  3: 12,
  4: 16,
  5: 20,
  6: 24,
  8: 32,
  10: 40,
  12: 48,
  16: 64,
};

// Common patterns
const layout = {
  screenPadding: 16,
  cardPadding: 16,
  sectionGap: 24,
  itemGap: 12,
};
```

## Shadows / Elevation

### iOS Shadows
```javascript
const iosShadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.1,
    shadowRadius: 2,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.15,
    shadowRadius: 8,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.2,
    shadowRadius: 16,
  },
};
```

### Android Elevation
```javascript
const androidElevation = {
  sm: { elevation: 2 },
  md: { elevation: 4 },
  lg: { elevation: 8 },
};
```

## Border Radius

```javascript
const borderRadius = {
  none: 0,
  sm: 4,
  md: 8,
  lg: 12,
  xl: 16,
  '2xl': 24,
  full: 9999,
};
```

## Theme Provider Pattern

```typescript
import React, { createContext, useContext } from 'react';
import { useColorScheme } from 'react-native';

const ThemeContext = createContext(null);

export const ThemeProvider = ({ children }) => {
  const colorScheme = useColorScheme();
  const isDark = colorScheme === 'dark';
  
  const theme = {
    colors: isDark ? darkColors : lightColors,
    typography,
    spacing,
    borderRadius,
  };
  
  return (
    <ThemeContext.Provider value={theme}>
      {children}
    </ThemeContext.Provider>
  );
};

export const useTheme = () => useContext(ThemeContext);
```
