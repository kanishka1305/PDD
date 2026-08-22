// ═══════════════════════════════════════════════════════════
// DentAI Mobile — Shared UI Components
// All styled to match the web dark medical theme exactly
// ═══════════════════════════════════════════════════════════
import React, { ReactNode } from 'react';
import {
  View, Text, TextInput, TouchableOpacity, ActivityIndicator,
  StyleSheet, ViewStyle, TextStyle, TextInputProps,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import { colors, spacing, radius, typography, shadows, gradients } from '../utils/theme';

// ── Card ──────────────────────────────────────────────────
export const Card = ({ children, style }: { children: ReactNode; style?: ViewStyle }) => (
  <View style={[styles.card, style]}>{children}</View>
);

export const CardHeader = ({
  title, subtitle, action,
}: { title: string; subtitle?: string; action?: ReactNode }) => (
  <View style={styles.cardHeader}>
    <View style={{ flex: 1 }}>
      <Text style={styles.cardHeaderLabel}>{title}</Text>
      {subtitle && <Text style={styles.cardSubtitle}>{subtitle}</Text>}
    </View>
    {action}
  </View>
);

// ── Gradient Button ───────────────────────────────────────
interface ButtonProps {
  onPress: () => void;
  label: string;
  icon?: ReactNode;
  loading?: boolean;
  disabled?: boolean;
  variant?: 'primary' | 'outline' | 'ghost' | 'danger';
  size?: 'sm' | 'md' | 'lg';
  fullWidth?: boolean;
  style?: ViewStyle;
}

export const Button = ({
  onPress, label, icon, loading, disabled,
  variant = 'primary', size = 'md', fullWidth = false, style,
}: ButtonProps) => {
  const isDisabled = disabled || loading;
  const heights = { sm: 36, md: 46, lg: 52 };
  const fontSizes = { sm: 12, md: 14, lg: 16 };

  if (variant === 'primary') {
    return (
      <TouchableOpacity
        onPress={onPress}
        disabled={isDisabled}
        activeOpacity={0.85}
        style={[{ width: fullWidth ? '100%' : undefined }, style]}>
        <LinearGradient
          colors={isDisabled ? ['#2a3a50', '#1e2d40'] : gradients.accent}
          start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
          style={[styles.btnGrad, { height: heights[size], opacity: isDisabled ? 0.5 : 1 }]}>
          {loading ? (
            <ActivityIndicator color={colors.white} size="small" />
          ) : (
            <>
              {icon && <View style={{ marginRight: 8 }}>{icon}</View>}
              <Text style={[styles.btnLabel, { fontSize: fontSizes[size] }]}>{label}</Text>
            </>
          )}
        </LinearGradient>
      </TouchableOpacity>
    );
  }

  const outlineStyles: ViewStyle = {
    height: heights[size],
    borderWidth: 1.5,
    borderColor: variant === 'danger' ? colors.danger : colors.borderMid,
    backgroundColor: 'transparent',
    borderRadius: radius.md,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: spacing.xl,
    opacity: isDisabled ? 0.45 : 1,
  };
  const textColor = variant === 'danger' ? colors.danger : colors.textSecondary;

  return (
    <TouchableOpacity onPress={onPress} disabled={isDisabled} activeOpacity={0.8}
      style={[outlineStyles, { width: fullWidth ? '100%' : undefined }, style]}>
      {loading ? (
        <ActivityIndicator color={textColor} size="small" />
      ) : (
        <>
          {icon && <View style={{ marginRight: 8 }}>{icon}</View>}
          <Text style={[styles.btnLabel, { fontSize: fontSizes[size], color: textColor }]}>{label}</Text>
        </>
      )}
    </TouchableOpacity>
  );
};

// ── Input ──────────────────────────────────────────────────
interface InputProps extends TextInputProps {
  label?: string;
  error?: string;
  leftIcon?: ReactNode;
  rightIcon?: ReactNode;
  containerStyle?: ViewStyle;
}
export const Input = ({ label, error, leftIcon, rightIcon, containerStyle, style, ...rest }: InputProps) => (
  <View style={[styles.inputContainer, containerStyle]}>
    {label && <Text style={styles.inputLabel}>{label}</Text>}
    <View style={[styles.inputWrap, error ? { borderColor: colors.danger } : null]}>
      {leftIcon && <View style={styles.inputIcon}>{leftIcon}</View>}
      <TextInput
        placeholderTextColor={colors.textMuted}
        style={[
          styles.input,
          leftIcon  ? { paddingLeft: 44 } : null,
          rightIcon ? { paddingRight: 44 } : null,
          style,
        ]}
        {...rest}
      />
      {rightIcon && <View style={styles.inputIconRight}>{rightIcon}</View>}
    </View>
    {error && <Text style={styles.inputError}>{error}</Text>}
  </View>
);

// ── Badge ─────────────────────────────────────────────────
type BadgeVariant = 'info' | 'success' | 'warning' | 'danger' | 'purple';
export const Badge = ({ label, variant = 'info' }: { label: string; variant?: BadgeVariant }) => {
  const cfg: Record<BadgeVariant, { bg: string; text: string; border: string }> = {
    info:    { bg: 'rgba(59,130,246,.12)',  text: '#93c5fd', border: 'rgba(59,130,246,.3)' },
    success: { bg: 'rgba(34,197,94,.12)',   text: '#86efac', border: 'rgba(34,197,94,.3)'  },
    warning: { bg: 'rgba(245,158,11,.12)',  text: '#fcd34d', border: 'rgba(245,158,11,.3)' },
    danger:  { bg: 'rgba(239,68,68,.12)',   text: '#fca5a5', border: 'rgba(239,68,68,.3)'  },
    purple:  { bg: 'rgba(139,92,246,.12)',  text: '#c4b5fd', border: 'rgba(139,92,246,.3)' },
  };
  const c = cfg[variant];
  return (
    <View style={[styles.badge, { backgroundColor: c.bg, borderColor: c.border }]}>
      <Text style={[styles.badgeText, { color: c.text }]}>{label}</Text>
    </View>
  );
};

// ── Status Pill ───────────────────────────────────────────
type StatusType = 'online' | 'offline' | 'idle' | 'busy' | 'analysed' | 'uploaded' | 'pending';
export const StatusPill = ({ status }: { status: StatusType }) => {
  const cfg: Record<string, { bg: string; text: string; border: string; label: string }> = {
    online:   { bg: 'rgba(34,197,94,.12)',   text: '#86efac', border: 'rgba(34,197,94,.3)',   label: 'Online'   },
    offline:  { bg: 'rgba(239,68,68,.12)',   text: '#fca5a5', border: 'rgba(239,68,68,.3)',   label: 'Offline'  },
    idle:     { bg: 'rgba(245,158,11,.12)',  text: '#fcd34d', border: 'rgba(245,158,11,.3)',  label: 'Idle'     },
    busy:     { bg: 'rgba(139,92,246,.12)',  text: '#c4b5fd', border: 'rgba(139,92,246,.3)',  label: 'Busy'     },
    analysed: { bg: 'rgba(34,197,94,.12)',   text: '#86efac', border: 'rgba(34,197,94,.3)',   label: 'Analysed' },
    analyzed: { bg: 'rgba(34,197,94,.12)',   text: '#86efac', border: 'rgba(34,197,94,.3)',   label: 'Analysed' },
    uploaded: { bg: 'rgba(245,158,11,.12)',  text: '#fcd34d', border: 'rgba(245,158,11,.3)',  label: 'Uploaded' },
    pending:  { bg: 'rgba(245,158,11,.12)',  text: '#fcd34d', border: 'rgba(245,158,11,.3)',  label: 'Pending'  },
  };
  const c = cfg[status] || cfg.idle;
  return (
    <View style={[styles.badge, { backgroundColor: c.bg, borderColor: c.border }]}>
      <Text style={[styles.badgeText, { color: c.text }]}>{c.label}</Text>
    </View>
  );
};

// ── Stat Card ─────────────────────────────────────────────
type StatColor = 'blue' | 'cyan' | 'green' | 'amber' | 'purple' | 'rose';
export const StatCard = ({
  label, value, sub, color = 'blue',
}: { label: string; value: string; sub?: string; color?: StatColor }) => {
  const colorMap: Record<StatColor, string> = {
    blue: colors.accent, cyan: colors.accent2, green: colors.success,
    amber: colors.warning, purple: colors.purple, rose: '#f43f5e',
  };
  const bgMap: Record<StatColor, string> = {
    blue: 'rgba(59,130,246,.1)', cyan: 'rgba(6,182,212,.1)', green: 'rgba(34,197,94,.1)',
    amber: 'rgba(245,158,11,.1)', purple: 'rgba(139,92,246,.1)', rose: 'rgba(244,63,94,.1)',
  };
  return (
    <View style={styles.statCard}>
      <View style={[styles.statIcon, { backgroundColor: bgMap[color] }]}>
        <View style={[styles.statDot, { backgroundColor: colorMap[color] }]} />
      </View>
      <Text style={[styles.statValue, { color: colorMap[color] }]}>{value}</Text>
      <Text style={styles.statLabel}>{label}</Text>
      {sub && <Text style={styles.statSub}>{sub}</Text>}
    </View>
  );
};

// ── Divider ───────────────────────────────────────────────
export const Divider = ({ label }: { label?: string }) => (
  <View style={styles.divider}>
    <View style={styles.dividerLine} />
    {label && <Text style={styles.dividerLabel}>{label}</Text>}
    {label && <View style={styles.dividerLine} />}
  </View>
);

// ── Section Header ────────────────────────────────────────
export const SectionHeader = ({ title }: { title: string }) => (
  <Text style={styles.sectionHeader}>{title}</Text>
);

// ── Empty State ───────────────────────────────────────────
export const EmptyState = ({ title, subtitle, action }: {
  title: string; subtitle?: string; action?: ReactNode;
}) => (
  <View style={styles.emptyState}>
    <Text style={styles.emptyTitle}>{title}</Text>
    {subtitle && <Text style={styles.emptySub}>{subtitle}</Text>}
    {action && <View style={{ marginTop: spacing.lg }}>{action}</View>}
  </View>
);

// ── Skeleton ──────────────────────────────────────────────
export const Skeleton = ({ width, height, style }: {
  width?: number | string; height: number; style?: ViewStyle;
}) => (
  <View style={[styles.skeleton, { width: width as any, height }, style]} />
);

// ── Styles ────────────────────────────────────────────────
const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.bgCard,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.lg,
    padding: spacing.xl,
    marginBottom: spacing.lg,
    ...shadows.sm,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    justifyContent: 'space-between',
    marginBottom: spacing.lg,
  },
  cardHeaderLabel: {
    fontSize: typography.sizes.sm,
    fontWeight: typography.weights.bold,
    color: colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: 0.7,
  },
  cardSubtitle: {
    fontSize: typography.sizes.base,
    color: colors.textSecondary,
    marginTop: 4,
  },
  btnGrad: {
    borderRadius: radius.md,
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'center',
    paddingHorizontal: spacing.xl,
    ...shadows.glow,
  },
  btnLabel: {
    color: colors.white,
    fontWeight: typography.weights.semibold,
    letterSpacing: 0.1,
  },
  inputContainer: { marginBottom: spacing.lg },
  inputLabel: {
    fontSize: typography.sizes.xs,
    fontWeight: typography.weights.semibold,
    color: colors.textSecondary,
    marginBottom: 7,
    textTransform: 'uppercase',
    letterSpacing: 0.5,
  },
  inputWrap: {
    borderWidth: 1.5,
    borderColor: colors.border,
    borderRadius: radius.md,
    backgroundColor: colors.bgSurface,
    flexDirection: 'row',
    alignItems: 'center',
  },
  input: {
    flex: 1,
    paddingHorizontal: spacing.md,
    paddingVertical: 11,
    color: colors.textPrimary,
    fontSize: typography.sizes.md,
  },
  inputIcon: {
    position: 'absolute',
    left: 13,
    zIndex: 1,
  },
  inputIconRight: {
    position: 'absolute',
    right: 13,
    zIndex: 1,
  },
  inputError: {
    fontSize: typography.sizes.xs,
    color: colors.danger,
    marginTop: 5,
  },
  badge: {
    paddingHorizontal: 10,
    paddingVertical: 3,
    borderRadius: radius.full,
    borderWidth: 1,
    alignSelf: 'flex-start',
  },
  badgeText: {
    fontSize: typography.sizes.xs,
    fontWeight: typography.weights.bold,
    letterSpacing: 0.3,
  },
  statCard: {
    flex: 1,
    backgroundColor: colors.bgCard,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.lg,
    padding: spacing.lg,
    ...shadows.sm,
  },
  statIcon: {
    width: 36,
    height: 36,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.md,
  },
  statDot: {
    width: 10,
    height: 10,
    borderRadius: radius.full,
  },
  statValue: {
    fontSize: typography.sizes.xxxl,
    fontWeight: typography.weights.extrabold,
    lineHeight: 34,
    marginBottom: 3,
  },
  statLabel: {
    fontSize: typography.sizes.xs,
    fontWeight: typography.weights.bold,
    color: colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: 0.6,
  },
  statSub: {
    fontSize: typography.sizes.xs,
    color: colors.textMuted,
    marginTop: 2,
  },
  divider: {
    flexDirection: 'row',
    alignItems: 'center',
    marginVertical: spacing.xl,
    gap: spacing.md,
  },
  dividerLine: {
    flex: 1,
    height: 1,
    backgroundColor: colors.border,
  },
  dividerLabel: {
    fontSize: typography.sizes.xs,
    fontWeight: typography.weights.medium,
    color: colors.textMuted,
  },
  sectionHeader: {
    fontSize: typography.sizes.xs,
    fontWeight: typography.weights.bold,
    color: colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: 1,
    paddingVertical: spacing.sm,
    paddingHorizontal: spacing.sm,
  },
  emptyState: {
    alignItems: 'center',
    padding: spacing.xxxl,
  },
  emptyTitle: {
    fontSize: typography.sizes.md,
    fontWeight: typography.weights.semibold,
    color: colors.textSecondary,
    textAlign: 'center',
    marginBottom: spacing.sm,
  },
  emptySub: {
    fontSize: typography.sizes.base,
    color: colors.textMuted,
    textAlign: 'center',
  },
  skeleton: {
    backgroundColor: colors.bgRaised,
    borderRadius: radius.sm,
  },
});
