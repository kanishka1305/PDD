/**
 * WorkflowScreen — Step-by-step guide for using DentAI
 * Same backend as web app. Mobile-first UI/UX design.
 * Presented as a bottom-sheet modal from the dashboard.
 */
import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  StatusBar, Platform,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import { useNavigation } from '@react-navigation/native';
import { colors, spacing, radius, typography, shadows, gradients } from '../utils/theme';

// ── Step data (mirrors the web WorkflowPage) ─────────────────────────────────
const STEPS = [
  {
    number: '01',
    title:  'Create Your Account',
    desc:   'Register with your medical license number. Access is restricted to verified dental professionals.',
    detail: 'Go to Create Account, enter your full name, license number, email, and a secure password. After submission you can log in immediately.',
    icon:   '⊙',
    color:  '#3b82f6',
    bg:     'rgba(59,130,246,.12)',
  },
  {
    number: '02',
    title:  'Upload a CBCT Scan',
    desc:   'Import a DICOM file, NIfTI volume (.nii / .nii.gz), or a ZIP archive of DICOM slices.',
    detail: 'Tap the Upload tab, press "Select File", and choose your scan. Files up to 2 GB are supported. Ensure the file is a valid medical imaging format.',
    icon:   '↑',
    color:  '#06b6d4',
    bg:     'rgba(6,182,212,.12)',
  },
  {
    number: '03',
    title:  'Run AI Segmentation',
    desc:   'The AI pipeline normalises the volume, runs threshold segmentation, and partitions the mandible into 9 anatomical regions.',
    detail: 'After upload, press "Run AI Segmentation". The process takes 15–120 seconds depending on scan resolution. You will see live progress updates.',
    icon:   '⬡',
    color:  '#8b5cf6',
    bg:     'rgba(139,92,246,.12)',
  },
  {
    number: '04',
    title:  'Review Results',
    desc:   'Inspect volumetric metrics for each anatomical region: condylar heads, coronoids, ramus, body, and symphysis.',
    detail: 'Navigate to the Results tab. Each of the 9 regions shows its volume in mm³. Review cortical/trabecular breakdown, bone loss %, and nerve distance.',
    icon:   '◈',
    color:  '#22c55e',
    bg:     'rgba(34,197,94,.12)',
  },
  {
    number: '05',
    title:  'Download STL & DICOM',
    desc:   'Export the full mandible or individual regions as STL (3D printing / surgical planning) or DICOM.',
    detail: 'In the Results screen, tap "Download Full STL" for the complete mandible, or use the per-region buttons to export individual anatomical structures.',
    icon:   '⬇',
    color:  '#f59e0b',
    bg:     'rgba(245,158,11,.12)',
  },
  {
    number: '06',
    title:  'Manage Scan History',
    desc:   'Browse all past scans, search by patient name, filter by analysis status, and re-open any previous result.',
    detail: 'Use the History tab to find any scan by patient name or scan ID. Tap a row to open its results. Pull to refresh the list.',
    icon:   '◷',
    color:  '#f43f5e',
    bg:     'rgba(244,63,94,.12)',
  },
];

// ── Supported file formats ────────────────────────────────────────────────────
const FORMATS = [
  { ext: '.dcm',    label: 'DICOM',   desc: 'Single-slice or multi-frame',  color: '#3b82f6' },
  { ext: '.nii',    label: 'NIfTI',   desc: '3-D volumetric scan',          color: '#06b6d4' },
  { ext: '.nii.gz', label: 'NIfTI GZ',desc: 'Compressed NIfTI volume',      color: '#8b5cf6' },
  { ext: '.zip',    label: 'ZIP',     desc: 'Folder of DICOM slices',       color: '#22c55e' },
];

// ── Anatomical regions ────────────────────────────────────────────────────────
const REGIONS = [
  'Condylar Head (Left & Right)',
  'Coronoid Process (Left & Right)',
  'Angle & Ramus (Left & Right)',
  'Body (Left & Right)',
  'Symphyseal / Parasymphyseal',
];

export default function WorkflowScreen() {
  const navigation    = useNavigation<any>();
  const [expanded, setExpanded] = useState<number | null>(null);

  const toggle = (i: number) =>
    setExpanded(prev => (prev === i ? null : i));

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={colors.bgBase} />

      {/* ── Header ── */}
      <LinearGradient colors={['#0f1623', '#080c18']} style={styles.header}>
        <TouchableOpacity
          onPress={() => navigation.goBack()}
          style={styles.closeBtn}
          hitSlop={{ top: 10, bottom: 10, left: 10, right: 10 }}>
          <Text style={styles.closeTxt}>✕</Text>
        </TouchableOpacity>
        <View style={styles.headerContent}>
          <LinearGradient colors={gradients.accent} style={styles.headerIcon}>
            <Text style={{ fontSize: 22, color: '#fff' }}>⬡</Text>
          </LinearGradient>
          <Text style={styles.headerTitle}>How DentAI Works</Text>
          <Text style={styles.headerSub}>
            CBCT AI Segmentation · 6-step clinical workflow
          </Text>
        </View>
      </LinearGradient>

      <ScrollView
        contentContainerStyle={styles.scroll}
        showsVerticalScrollIndicator={false}>

        {/* ── Steps ── */}
        <Text style={styles.sectionLabel}>WORKFLOW STEPS</Text>
        {STEPS.map((step, i) => (
          <TouchableOpacity
            key={i}
            style={styles.stepCard}
            onPress={() => toggle(i)}
            activeOpacity={0.85}>

            {/* Number + title row */}
            <View style={styles.stepRow}>
              <View style={[styles.stepNumWrap, { backgroundColor: step.bg }]}>
                <Text style={[styles.stepNum, { color: step.color }]}>{step.number}</Text>
              </View>
              <View style={{ flex: 1 }}>
                <Text style={styles.stepTitle}>{step.title}</Text>
                <Text style={styles.stepDesc} numberOfLines={expanded === i ? undefined : 2}>
                  {step.desc}
                </Text>
              </View>
              <View style={[styles.stepIconBadge, { backgroundColor: step.bg }]}>
                <Text style={{ fontSize: 18, color: step.color }}>{step.icon}</Text>
              </View>
            </View>

            {/* Expanded detail */}
            {expanded === i && (
              <View style={[styles.stepDetail, { borderLeftColor: step.color }]}>
                <Text style={styles.stepDetailText}>{step.detail}</Text>
              </View>
            )}

            {/* Expand indicator */}
            <Text style={styles.stepExpand}>
              {expanded === i ? '▲ Less' : '▼ More'}
            </Text>
          </TouchableOpacity>
        ))}

        {/* ── Supported formats ── */}
        <Text style={styles.sectionLabel}>SUPPORTED FILE FORMATS</Text>
        <View style={styles.formatsGrid}>
          {FORMATS.map(f => (
            <View key={f.ext} style={[styles.formatCard, { borderColor: `${f.color}40` }]}>
              <View style={[styles.formatBadge, { backgroundColor: `${f.color}18` }]}>
                <Text style={[styles.formatExt, { color: f.color }]}>{f.ext}</Text>
              </View>
              <Text style={styles.formatLabel}>{f.label}</Text>
              <Text style={styles.formatDesc}>{f.desc}</Text>
            </View>
          ))}
        </View>

        {/* ── Anatomical regions ── */}
        <Text style={styles.sectionLabel}>9 ANATOMICAL REGIONS</Text>
        <View style={styles.regionsCard}>
          {REGIONS.map((r, i) => (
            <View key={i} style={styles.regionRow}>
              <LinearGradient
                colors={gradients.accent}
                style={styles.regionDot}
              />
              <Text style={styles.regionText}>{r}</Text>
            </View>
          ))}
        </View>

        {/* ── Technical note ── */}
        <View style={styles.noteCard}>
          <Text style={styles.noteTitle}>Technical Notes</Text>
          <Text style={styles.noteBody}>
            The AI uses threshold-based segmentation with a geometric mandible
            partition algorithm. No GPU or external ML inference service is
            required — processing runs entirely on the backend server.{'\n\n'}
            Single-slice (2D) DICOM files are supported via Y-axis partitioning
            as a fallback. 3D volumes (Z-depth ≥ 2 slices) use Z-axis partitioning
            for higher anatomical precision.
          </Text>
        </View>

        {/* ── CTA ── */}
        <TouchableOpacity
          style={styles.ctaBtn}
          onPress={() => navigation.goBack()}
          activeOpacity={0.85}>
          <LinearGradient
            colors={gradients.accent}
            start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
            style={styles.ctaGrad}>
            <Text style={styles.ctaText}>Start Uploading Scans  →</Text>
          </LinearGradient>
        </TouchableOpacity>

      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.bgBase },

  // ── Header ──────────────────────────────────────────────
  header: {
    paddingTop: Platform.select({ ios: 56, android: 48 }),
    paddingBottom: spacing.xl,
    paddingHorizontal: spacing.xl,
    borderBottomWidth: 1,
    borderBottomColor: colors.border,
  },
  closeBtn: {
    alignSelf: 'flex-end',
    padding: spacing.sm,
    marginBottom: spacing.md,
  },
  closeTxt: {
    fontSize: 16,
    color: colors.textMuted,
    fontWeight: '700',
  },
  headerContent: { alignItems: 'center' },
  headerIcon: {
    width: 60,
    height: 60,
    borderRadius: 16,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.md,
    ...shadows.glow,
  },
  headerTitle: {
    fontSize: typography.sizes.xxl,
    fontWeight: typography.weights.extrabold,
    color: colors.textPrimary,
    textAlign: 'center',
    letterSpacing: -0.3,
  },
  headerSub: {
    fontSize: typography.sizes.base,
    color: colors.textMuted,
    textAlign: 'center',
    marginTop: 6,
  },

  // ── Section label ───────────────────────────────────────
  sectionLabel: {
    fontSize: typography.sizes.xs,
    fontWeight: typography.weights.bold,
    color: colors.textMuted,
    textTransform: 'uppercase',
    letterSpacing: 1.2,
    marginBottom: spacing.md,
    marginTop: spacing.xl,
  },

  scroll: {
    padding: spacing.xl,
    paddingBottom: 100,
  },

  // ── Step card ───────────────────────────────────────────
  stepCard: {
    backgroundColor: colors.bgCard,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.lg,
    padding: spacing.lg,
    marginBottom: spacing.md,
    ...shadows.sm,
  },
  stepRow: {
    flexDirection: 'row',
    alignItems: 'flex-start',
    gap: spacing.md,
  },
  stepNumWrap: {
    width: 42,
    height: 42,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
  },
  stepNum: {
    fontSize: typography.sizes.base,
    fontWeight: typography.weights.extrabold,
    letterSpacing: 0.5,
  },
  stepTitle: {
    fontSize: typography.sizes.md,
    fontWeight: typography.weights.bold,
    color: colors.textPrimary,
    marginBottom: 4,
  },
  stepDesc: {
    fontSize: typography.sizes.base,
    color: colors.textSecondary,
    lineHeight: 19,
  },
  stepIconBadge: {
    width: 36,
    height: 36,
    borderRadius: radius.md,
    alignItems: 'center',
    justifyContent: 'center',
    flexShrink: 0,
  },
  stepDetail: {
    marginTop: spacing.md,
    paddingLeft: spacing.md,
    borderLeftWidth: 3,
    paddingVertical: spacing.sm,
  },
  stepDetailText: {
    fontSize: typography.sizes.base,
    color: colors.textSecondary,
    lineHeight: 20,
  },
  stepExpand: {
    fontSize: typography.sizes.xs,
    color: colors.accent,
    fontWeight: typography.weights.semibold,
    marginTop: spacing.sm,
    textAlign: 'right',
  },

  // ── Formats ─────────────────────────────────────────────
  formatsGrid: {
    flexDirection: 'row',
    flexWrap: 'wrap',
    gap: spacing.sm,
    marginBottom: spacing.sm,
  },
  formatCard: {
    width: '47%',
    backgroundColor: colors.bgCard,
    borderWidth: 1,
    borderRadius: radius.md,
    padding: spacing.md,
    ...shadows.sm,
  },
  formatBadge: {
    alignSelf: 'flex-start',
    paddingHorizontal: 10,
    paddingVertical: 3,
    borderRadius: radius.full,
    marginBottom: spacing.sm,
  },
  formatExt: {
    fontSize: typography.sizes.xs,
    fontWeight: typography.weights.extrabold,
    letterSpacing: 0.3,
  },
  formatLabel: {
    fontSize: typography.sizes.base,
    fontWeight: typography.weights.bold,
    color: colors.textPrimary,
    marginBottom: 2,
  },
  formatDesc: {
    fontSize: typography.sizes.xs,
    color: colors.textMuted,
  },

  // ── Regions ─────────────────────────────────────────────
  regionsCard: {
    backgroundColor: colors.bgCard,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.lg,
    padding: spacing.lg,
    ...shadows.sm,
  },
  regionRow: {
    flexDirection: 'row',
    alignItems: 'center',
    gap: spacing.md,
    paddingVertical: spacing.sm,
    borderBottomWidth: 1,
    borderBottomColor: 'rgba(30,45,64,.5)',
  },
  regionDot: {
    width: 8,
    height: 8,
    borderRadius: 4,
    flexShrink: 0,
  },
  regionText: {
    fontSize: typography.sizes.base,
    color: colors.textSecondary,
  },

  // ── Note ────────────────────────────────────────────────
  noteCard: {
    backgroundColor: 'rgba(59,130,246,.07)',
    borderWidth: 1,
    borderColor: 'rgba(59,130,246,.2)',
    borderRadius: radius.lg,
    padding: spacing.lg,
    marginTop: spacing.xl,
  },
  noteTitle: {
    fontSize: typography.sizes.base,
    fontWeight: typography.weights.bold,
    color: colors.accent,
    marginBottom: spacing.sm,
  },
  noteBody: {
    fontSize: typography.sizes.base,
    color: colors.textSecondary,
    lineHeight: 20,
  },

  // ── CTA ─────────────────────────────────────────────────
  ctaBtn: {
    marginTop: spacing.xxl,
    borderRadius: radius.md,
    overflow: 'hidden',
    ...shadows.glow,
  },
  ctaGrad: {
    height: 52,
    alignItems: 'center',
    justifyContent: 'center',
  },
  ctaText: {
    fontSize: typography.sizes.md,
    fontWeight: typography.weights.bold,
    color: colors.white,
    letterSpacing: 0.2,
  },
});
