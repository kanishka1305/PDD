// ═══════════════════════════════════════════════════════════
// DentAI Mobile — Theme (matches web CSS variables exactly)
// ═══════════════════════════════════════════════════════════
import { Dimensions } from 'react-native';

const { width: SCREEN_WIDTH, height: SCREEN_HEIGHT } = Dimensions.get('window');

export const colors = {
  // Backgrounds
  bgBase:    '#080c18',
  bgSurface: '#0f1623',
  bgCard:    '#111827',
  bgRaised:  '#1a2236',
  bgHover:   '#1e2a3d',

  // Borders
  border:    '#1e2d40',
  borderMid: '#2a3a50',

  // Text
  textPrimary:   '#e8edf5',
  textSecondary: '#8b96a8',
  textMuted:     '#4b5a6d',

  // Accent
  accent:  '#3b82f6',
  accent2: '#06b6d4',

  // Status
  success: '#22c55e',
  warning: '#f59e0b',
  danger:  '#ef4444',
  purple:  '#8b5cf6',

  // Gradient stops
  gradStart: '#3b82f6',
  gradEnd:   '#06b6d4',

  white: '#ffffff',
  black: '#000000',
  transparent: 'transparent',
};

export const gradients = {
  accent:   [colors.gradStart, colors.gradEnd] as const,
  dark:     ['#1a2236', '#111827'] as const,
  surface:  ['#0f1623', '#080c18'] as const,
  success:  ['#16a34a', '#22c55e'] as const,
  danger:   ['#dc2626', '#ef4444'] as const,
  card:     ['#1a2236', '#111827'] as const,
  purple:   ['#7c3aed', '#8b5cf6'] as const,
};

export const spacing = {
  xs: 4,
  sm: 8,
  md: 12,
  lg: 16,
  xl: 20,
  xxl: 24,
  xxxl: 32,
  section: 40,
};

export const radius = {
  sm: 6,
  md: 10,
  lg: 14,
  xl: 20,
  full: 999,
};

export const typography = {
  fontFamily: 'System',
  sizes: {
    xs:   10,
    sm:   11,
    base: 13,
    md:   14,
    lg:   16,
    xl:   18,
    xxl:  22,
    xxxl: 28,
    hero: 34,
  },
  weights: {
    regular:   '400' as const,
    medium:    '500' as const,
    semibold:  '600' as const,
    bold:      '700' as const,
    extrabold: '800' as const,
  },
};

export const shadows = {
  sm: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 1 },
    shadowOpacity: 0.4,
    shadowRadius: 3,
    elevation: 3,
  },
  md: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 4 },
    shadowOpacity: 0.45,
    shadowRadius: 12,
    elevation: 6,
  },
  lg: {
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.55,
    shadowRadius: 24,
    elevation: 12,
  },
  glow: {
    shadowColor: colors.accent,
    shadowOffset: { width: 0, height: 0 },
    shadowOpacity: 0.35,
    shadowRadius: 12,
    elevation: 8,
  },
};

export const layout = {
  screenWidth:  SCREEN_WIDTH,
  screenHeight: SCREEN_HEIGHT,
  headerHeight: 60,
  tabBarHeight: 60,
  sidebarWidth: 256,
  cardPadding: spacing.xl,
};
