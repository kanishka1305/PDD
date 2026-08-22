import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  Alert, Platform, StatusBar, ActivityIndicator,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import DocumentPicker from 'react-native-document-picker';
import { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import { colors, spacing, radius, shadows, gradients } from '../utils/theme';
import { Card, CardHeader, Button, Badge } from '../components/UI';
import { api } from '../api/client';
import { MainTabParamList } from '../navigation/types';

type Props = { navigation: BottomTabNavigationProp<MainTabParamList, 'Upload'> };

const STEPS = ['Select File', 'Verify Info', 'Upload', 'AI Analysis'];
const ALLOWED_EXTS = ['.dcm', '.nii', '.nii.gz', '.zip'];

export default function UploadScreen({ navigation }: Props) {
  const [file, setFile]           = useState<any>(null);
  const [step, setStep]           = useState(0);
  const [uploading, setUploading] = useState(false);
  const [analysing, setAnalysing] = useState(false);
  const [uploadPct, setUploadPct] = useState(0);
  const [scanId, setScanId]       = useState<number | null>(null);
  const [metadata, setMetadata]   = useState<any>(null);
  const [error, setError]         = useState('');

  const pickFile = async () => {
    try {
      const result = await DocumentPicker.pick({
        type: [DocumentPicker.types.allFiles],
        copyTo: 'cachesDirectory',
      });
      const picked = result[0];
      const name = picked.name || '';
      const lower = name.toLowerCase();
      const valid = ALLOWED_EXTS.some(e => lower.endsWith(e));
      if (!valid) { setError('Unsupported format. Please upload .dcm, .nii, .nii.gz or .zip.'); return; }
      if ((picked.size || 0) === 0) { setError('File appears to be empty.'); return; }
      setError('');
      setFile(picked);
      setStep(1);
    } catch (e) {
      if (!DocumentPicker.isCancel(e)) setError('File pick failed.');
    }
  };

  const clearFile = () => {
    setFile(null); setStep(0); setScanId(null);
    setMetadata(null); setError(''); setUploadPct(0);
  };

  const handleUpload = async () => {
    if (!file) return;
    setUploading(true); setStep(2); setUploadPct(0); setError('');
    // Animate progress
    const interval = setInterval(() => {
      setUploadPct(p => (p < 92 ? p + 3 : p));
    }, 120);
    try {
      const uri = file.fileCopyUri || file.uri;
      const res = await api.uploadScan(uri, file.name, file.type || 'application/octet-stream');
      clearInterval(interval); setUploadPct(100);
      if (res.data.error) { setError('Upload error: ' + res.data.error); setUploading(false); return; }
      setScanId(res.data.scan_id);
      setMetadata(res.data.metadata || {});
      setStep(3);
    } catch (err: any) {
      clearInterval(interval);
      setError('Upload failed. Make sure the backend is running.');
    } finally { setUploading(false); }
  };

  const handleAnalyse = async () => {
    if (!scanId) return;
    setAnalysing(true); setError('');
    try {
      await api.analyze(scanId);
      navigation.navigate('Results', { scanId });
    } catch (err: any) {
      setError('Analysis failed: ' + (err.message || 'Unknown error'));
    } finally { setAnalysing(false); }
  };

  const fmtSize = (bytes: number) => {
    if (!bytes) return '—';
    if (bytes >= 1073741824) return (bytes / 1073741824).toFixed(2) + ' GB';
    if (bytes >= 1048576) return (bytes / 1048576).toFixed(1) + ' MB';
    return (bytes / 1024).toFixed(0) + ' KB';
  };

  const fileType = file ? (
    file.name?.toLowerCase().endsWith('.nii.gz') ? 'NIfTI GZ' :
    file.name?.toLowerCase().endsWith('.nii') ? 'NIfTI' :
    file.name?.toLowerCase().endsWith('.zip') ? 'ZIP' : 'DICOM'
  ) : '';

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={colors.bgBase} />
      <View style={styles.header}>
        <Text style={styles.title}>Upload Scan</Text>
        <Text style={styles.subtitle}>Import DICOM, NIfTI or ZIP for AI segmentation</Text>
      </View>

      {/* Step Indicator */}
      <View style={styles.stepRow}>
        {STEPS.map((label, i) => (
          <React.Fragment key={i}>
            <View style={styles.stepItem}>
              <View style={[styles.stepNum, i < step && styles.stepDone, i === step && styles.stepActive]}>
                {i < step
                  ? <Text style={{ color: '#fff', fontSize: 11, fontWeight: '700' }}>✓</Text>
                  : <Text style={{ color: i === step ? '#fff' : colors.textMuted, fontSize: 11, fontWeight: '700' }}>{i + 1}</Text>
                }
              </View>
              <Text style={[styles.stepLabel, i === step && { color: colors.accent }]} numberOfLines={1}>{label}</Text>
            </View>
            {i < STEPS.length - 1 && (
              <View style={[styles.stepLine, i < step && { backgroundColor: colors.success }]} />
            )}
          </React.Fragment>
        ))}
      </View>

      <ScrollView contentContainerStyle={styles.scroll} showsVerticalScrollIndicator={false}>

        {/* Error */}
        {!!error && (
          <View style={styles.alertError}>
            <Text style={{ color: '#fca5a5', fontSize: 13 }}>{error}</Text>
          </View>
        )}

        {/* Step 0 — Drop Zone */}
        {step === 0 && (
          <TouchableOpacity style={styles.dropZone} onPress={pickFile} activeOpacity={0.85}>
            <LinearGradient colors={['rgba(59,130,246,.15)', 'rgba(6,182,212,.08)']} style={styles.dropInner}>
              <View style={styles.dropIcon}>
                <Text style={{ fontSize: 36 }}>⬆️</Text>
              </View>
              <Text style={styles.dropTitle}>Tap to select a scan file</Text>
              <Text style={styles.dropSub}>or drag from your files app</Text>
              <View style={styles.fmtRow}>
                {['.dcm', '.nii', '.nii.gz', '.zip'].map(f => (
                  <View key={f} style={styles.fmtBadge}>
                    <Text style={styles.fmtText}>{f}</Text>
                  </View>
                ))}
              </View>
              <Text style={styles.dropHint}>Max file size: 2 GB · Processed locally</Text>
            </LinearGradient>
          </TouchableOpacity>
        )}

        {/* Step 1 — File Preview + Upload */}
        {(step === 1 || step === 2) && file && (
          <Card>
            <View style={styles.fileRow}>
              <LinearGradient colors={gradients.accent} style={styles.fileIcon}>
                <Text style={{ fontSize: 22 }}>📁</Text>
              </LinearGradient>
              <View style={{ flex: 1 }}>
                <Text style={styles.fileName} numberOfLines={2}>{file.name}</Text>
                <Text style={styles.fileMeta}>{fileType} · {fmtSize(file.size)}</Text>
              </View>
              {step === 1 && (
                <TouchableOpacity onPress={clearFile} style={styles.clearBtn}>
                  <Text style={{ color: colors.textMuted, fontSize: 16 }}>✕</Text>
                </TouchableOpacity>
              )}
            </View>

            {step === 2 && (
              <View style={{ marginTop: spacing.lg }}>
                <View style={{ flexDirection: 'row', justifyContent: 'space-between', marginBottom: 8 }}>
                  <Text style={{ fontSize: 13, color: colors.textSecondary }}>
                    {uploadPct < 100 ? 'Uploading…' : 'Upload complete!'}
                  </Text>
                  <Text style={{ fontSize: 13, fontWeight: '700', color: colors.accent }}>{uploadPct}%</Text>
                </View>
                <View style={styles.progressBg}>
                  <LinearGradient
                    colors={gradients.accent}
                    start={{ x: 0, y: 0 }} end={{ x: 1, y: 0 }}
                    style={[styles.progressFill, { width: `${uploadPct}%` as any }]}
                  />
                </View>
              </View>
            )}

            {step === 1 && (
              <Button
                onPress={handleUpload}
                label="Upload Scan"
                loading={uploading}
                fullWidth
                style={{ marginTop: spacing.lg }}
              />
            )}
          </Card>
        )}

        {/* Step 3 — Metadata + Analyse */}
        {step === 3 && metadata && scanId && (
          <Card>
            <CardHeader title="Scan Metadata" action={<Badge label="Uploaded" variant="success" />} />
            <MetaRow label="Scan ID" value={`#${scanId}`} />
            <MetaRow label="Patient Name" value={metadata.patient_name || metadata.PatientName || 'N/A'} />
            <MetaRow label="Patient ID" value={metadata.patient_id || metadata.PatientID || 'N/A'} />
            <MetaRow label="Modality" value={metadata.modality || 'CBCT'} />
            <MetaRow label="Dimensions" value={metadata.image_shape ? metadata.image_shape.join(' × ') : '—'} />
            <MetaRow label="Study Date" value={metadata.study_date || metadata.StudyDate || '—'} />

            <View style={{ marginTop: spacing.xl, gap: spacing.md }}>
              {analysing && (
                <View style={{ alignItems: 'center', paddingVertical: spacing.lg }}>
                  <ActivityIndicator color={colors.accent} size="large" />
                  <Text style={{ color: colors.textSecondary, marginTop: spacing.md, fontSize: 13 }}>
                    Running AI segmentation…
                  </Text>
                  <Text style={{ color: colors.textMuted, fontSize: 11, marginTop: 4 }}>
                    This may take 30–120 seconds
                  </Text>
                </View>
              )}
              {!analysing && (
                <>
                  <Button onPress={handleAnalyse} label="Run AI Segmentation" fullWidth />
                  <Button onPress={clearFile} label="Upload Another" variant="outline" fullWidth />
                </>
              )}
            </View>
          </Card>
        )}

      </ScrollView>
    </View>
  );
}

const MetaRow = ({ label, value }: { label: string; value: string }) => (
  <View style={{ flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 9, borderBottomWidth: 1, borderBottomColor: 'rgba(30,45,64,.5)' }}>
    <Text style={{ fontSize: 12, color: colors.textSecondary }}>{label}</Text>
    <Text style={{ fontSize: 12, fontWeight: '600', color: colors.textPrimary, flex: 1, textAlign: 'right' }}>{value}</Text>
  </View>
);

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.bgBase },
  header: { paddingHorizontal: spacing.xl, paddingTop: 52, paddingBottom: spacing.lg, borderBottomWidth: 1, borderBottomColor: colors.border, backgroundColor: colors.bgSurface },
  title: { fontSize: 22, fontWeight: '700', color: colors.textPrimary },
  subtitle: { fontSize: 12, color: colors.textMuted, marginTop: 2 },
  stepRow: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: spacing.lg, paddingVertical: spacing.md, backgroundColor: colors.bgCard, borderBottomWidth: 1, borderBottomColor: colors.border },
  stepItem: { alignItems: 'center', gap: 4 },
  stepNum: { width: 26, height: 26, borderRadius: 13, backgroundColor: colors.bgRaised, borderWidth: 2, borderColor: colors.border, alignItems: 'center', justifyContent: 'center' },
  stepActive: { backgroundColor: colors.accent, borderColor: colors.accent },
  stepDone: { backgroundColor: colors.success, borderColor: colors.success },
  stepLabel: { fontSize: 9, color: colors.textMuted, fontWeight: '600', textAlign: 'center', maxWidth: 60 },
  stepLine: { flex: 1, height: 2, backgroundColor: colors.border, marginBottom: 12 },
  scroll: { padding: spacing.lg, paddingBottom: 100 },
  alertError: { backgroundColor: 'rgba(239,68,68,.1)', borderWidth: 1, borderColor: 'rgba(239,68,68,.4)', borderRadius: radius.md, padding: spacing.md, marginBottom: spacing.lg },
  dropZone: { borderRadius: radius.lg, overflow: 'hidden', marginBottom: spacing.lg, ...shadows.md },
  dropInner: { padding: spacing.xxxl, alignItems: 'center', borderWidth: 2, borderColor: 'rgba(59,130,246,.3)', borderRadius: radius.lg, borderStyle: 'dashed' },
  dropIcon: { width: 80, height: 80, borderRadius: 40, backgroundColor: 'rgba(59,130,246,.1)', alignItems: 'center', justifyContent: 'center', marginBottom: spacing.xl },
  dropTitle: { fontSize: 18, fontWeight: '700', color: colors.textPrimary, marginBottom: 6, textAlign: 'center' },
  dropSub: { fontSize: 13, color: colors.textSecondary, marginBottom: spacing.xl, textAlign: 'center' },
  fmtRow: { flexDirection: 'row', gap: 8, flexWrap: 'wrap', justifyContent: 'center', marginBottom: spacing.md },
  fmtBadge: { paddingHorizontal: 12, paddingVertical: 4, borderRadius: radius.full, backgroundColor: 'rgba(59,130,246,.1)', borderWidth: 1, borderColor: 'rgba(59,130,246,.3)' },
  fmtText: { fontSize: 11, fontWeight: '700', color: '#93c5fd' },
  dropHint: { fontSize: 11, color: colors.textMuted, textAlign: 'center' },
  fileRow: { flexDirection: 'row', alignItems: 'center', gap: spacing.md },
  fileIcon: { width: 48, height: 48, borderRadius: radius.md, alignItems: 'center', justifyContent: 'center' },
  fileName: { fontSize: 14, fontWeight: '700', color: colors.textPrimary, marginBottom: 3 },
  fileMeta: { fontSize: 11, color: colors.textMuted },
  clearBtn: { padding: 8 },
  progressBg: { height: 8, backgroundColor: colors.bgRaised, borderRadius: 4, overflow: 'hidden' },
  progressFill: { height: 8, borderRadius: 4 },
});
