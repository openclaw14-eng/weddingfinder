// Weddingfinder Theme Constants

const THEME = {
  colors: {
    // Primary - Pink
    primary: '#ec4899',
    primaryLight: '#f472b6',
    primaryDark: '#db2777',
    primary50: '#fdf2f8',
    primary100: '#fce7f3',
    primary200: '#fbcfe8',
    primary300: '#f9a8d4',
    primary400: '#f472b6',
    primary500: '#ec4899',
    primary600: '#db2777',
    primary700: '#be185d',
    
    // Accent - Gold
    accent: '#f59e0b',
    accentLight: '#fbbf24',
    accentDark: '#d97706',
    accent50: '#fffbeb',
    accent100: '#fef3c7',
    accent200: '#fde68a',
    accent300: '#fcd34d',
    accent400: '#fbbf24',
    accent500: '#f59e0b',
    accent600: '#d97706',
    accent700: '#b45309',
    
    // Neutrals
    white: '#ffffff',
    gray50: '#f9fafb',
    gray100: '#f3f4f6',
    gray200: '#e5e7eb',
    gray300: '#d1d5db',
    gray400: '#9ca3af',
    gray500: '#6b7280',
    gray600: '#4b5563',
    gray700: '#374151',
    gray800: '#1f2937',
    gray900: '#111827',
    black: '#000000',
    
    // Semantic
    success: '#10b981',
    error: '#ef4444',
    warning: '#f59e0b',
    info: '#3b82f6'
  },
  
  fonts: {
    heading: "'Playfair Display', Georgia, serif",
    body: "'Inter', -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, sans-serif"
  },
  
  shadows: {
    sm: '0 1px 2px 0 rgba(0, 0, 0, 0.05)',
    md: '0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1)',
    lg: '0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1)',
    xl: '0 20px 25px -5px rgba(0, 0, 0, 0.1), 0 8px 10px -6px rgba(0, 0, 0, 0.1)',
    pink: '0 4px 14px 0 rgba(236, 72, 153, 0.39)',
    gold: '0 4px 14px 0 rgba(245, 158, 11, 0.39)'
  },
  
  radii: {
    sm: '4px',
    md: '8px',
    lg: '12px',
    xl: '16px',
    full: '9999px'
  },
  
  spacing: {
    xs: '0.25rem',   // 4px
    sm: '0.5rem',    // 8px
    md: '1rem',      // 16px
    lg: '1.5rem',    // 24px
    xl: '2rem',      // 32px
    '2xl': '3rem',   // 48px
    '3xl': '4rem'    // 64px
  }
};

// Export for use in other files
if (typeof module !== 'undefined' && module.exports) {
  module.exports = { THEME };
}
