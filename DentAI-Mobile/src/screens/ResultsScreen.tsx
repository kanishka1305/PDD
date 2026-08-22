import React, { useState, useEffect } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  Linking, StatusBar, Alert,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import { RouteProp } from '@react-navigation/native';
import { colors, spacing, radius, shadows, gradients } from '../utils/theme';
import { Card, CardHeader, Badge, Button, EmptyState, Skeleton } from '../components/UI';
import { api, BASE_URL } from '../api/client';
import { MainTabParamList } from '../navigation/types';

type Props = {
  navigation: BottomTabNavigationProp<MainTabParamList, 'Results'>;
  route: RouteProp<MainTabParamList, 'Results'>;
};

const REGIONS = [
  { key: 'condylar_head_L', label: 'Condylar Head L', color: '#3b82f6', short: 'CHL' },
  { key: 'condylar_head_R', label: 'Condylar Head R', color: '#60a5fa', short: 'CHR' },
  { key: 'coronoid_L',      label: 'Coronoid L',      color: '#06b6d4', short: 'CNL' },
  { key: 'coronoid_R',      label: 'Coronoid R',      color: '#22d3ee', short: 'CNR' },
  { key: 'angle_ramus_L',   label: 'Ramus L',         color: '#8b5cf6', short: 'ARL' },
  { key: 'angle_ramus_R',   label: 'Ramus R',         color: '#a78bfa', short: 'ARR' },
  { key: 'full',            label: 'Full Mandible',   color: '#f59e0b', short: 'FULL' },
];

export default function ResultsScreen({ navigation, route }: Props) {
  const scanId = route.params?.scanId;
  const [scans, setScans]     = useState<any[]>([]);
  const [selected, setSelected] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [result, setResult]   = useState<any>(null);

  useEffect(() => {
    loadData();
  }, [scanId]);

  const loadData = async () => {
    try {
      const res = await api.getScans();
      const all = res.data.scans || [];
      setScans(all);
      if (scanId) {
        const found = all.find((s: any) => s.id === scanId);
        if (found) { setSelected(found); loadResult(scanId); }
      } else if (all.length > 0) {
        const latest = all.find((s: any) => s.status === 'analysed' || s.status === 'analyzed') || all[0];
        setSelected(latest);
        if (latest?.status === 'analysed' || latest?.status === 'analyzed') loadResult(latest.id);
      }
    } catch {}
    finally { setLoading(false); }
  };

  const loadResult = async (id: number) => {
    try {
      const stored = result;
      // Results come from localStorage equivalent in real app
      setResult(null); // placeholder
    } catch {}
  };

  const openDownload = (url: string) => {
    Linking.openURL(url).catch(() =>
      Alert.alert('Error', 'Could not open download link.')
    );
  };

  if (loading) {
    return (
      <View style={styles.container}>
        <StatusBar barStyle="light-content" backgroundColor={colors.bgBase} />
        <View style={styles.header}>
          <Skeleton width={160} height={22} style={{ marginBottom: 8 }} />
          <Skeleton width={100} height={13} />
        </View>
        <ScrollView contentContainerStyle={styles.scroll}>
          {[0,1,2].map(i => (
            <View key={i} style={{ backgroundColor: colors.bgCard, borderRadius: radius.lg, padding: spacing.xl, marginBottom: spacing.lg }}>
              <Skeleton width="80%" height={14} style={{ marginBottom: 12 }} />
              <Skeleton width="60%" height={12} style={{ marginBottom: 8 }} />
              <Skeleton width="70%" height={12} />
            </View>
          ))}
        </ScrollView>
      </View>
    );
  }

  if (!selected) {
    return (
      <View style={[styles.container, { justifyContent: 'center', alignItems: 'center' }]}>
        <EmptyState
          title="No analysis results yet"
          subtitle="Upload and analyse a CBCT scan first"
          action={
            <Button label="Upload Scan" onPress={() => navigation.navigate('Upload')} />
          }
        />
      </View>
    );
  }

  const isAnalysed = selected.status === 'analysed' || selected.status === 'analyzed';

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={colors.bgBase} />

      {/* Header */}
      <View style={styles.header}>
        <View>
          <Text style={styles.title}>Results</Text>
          <Text style={styles.subtitle}>Scan #{selected.id} · {selected.patient_name || 'Unknown Patient'}</Text>
        </View>
        <Badge label={isAnalysed ? 'Analysed' : 'Pending'} variant={isAnalysed ? 'success' : 'warning'} />
      </View>

      <ScrollView contentContainerStyle={styles.scroll} showsVerticalScrollIndicator={false}>

        {/* Scan selector */}
        {scans.length > 1 && (
          <ScrollView horizontal showsHorizontalScrollIndicator={false} style={{ marginBottom: spacing.lg }}>
            <View style={{ flexDirection: 'row', gap: spacing.sm, paddingHorizontal: 2 }}>
              {scans.slice(0, 10).map(s => (
                <TouchableOpacity
                  key={s.id}
                  onPress={() => { setSelected(s); loadResult(s.id); }}
                  style={[styles.scanChip, selected?.id === s.id && styles.scanChipActive]}>
                  <Text style={[styles.scanChipText, selected?.id === s.id && { color: colors.accent }]}>
                    #{s.id}
                  </Text>
                </TouchableOpacity>
              ))}
            </View>
          </ScrollView>
        )}

        {/* Patient Info */}
        <Card>
          <CardHeader title="Patient Information" />
          <View style={styles.infoGrid}>
            <InfoCell label="Patient Name" value={selected.patient_name || 'N/A'} />
            <InfoCell label="Modality" value={selected.modality || 'CBCT'} />
            <InfoCell label="Scan ID" value={`#${selected.id}`} />
            <InfoCell label="Status" value={isAnalysed ? 'Analysed' : 'Pending'} />
          </View>
        </Card>

        {/* Regions */}
        {isAnalysed ? (
          <Card>
            <CardHeader title="Segmented Regions" subtitle="Tap a region to download STL or DICOM" />
            <View style={styles.regionGrid}>
              {REGIONS.map(r => (
                <RegionCard
                  key={r.key}
                  region={r}
                  scanId={selected.id}
                  onStl={() => openDownload(`${BASE_URL}/stl-region/${selected.id}/${r.key}`)}
                  onDcm={() => openDownload(`${BASE_URL}/export-dicom/${selected.id}/${r.key}`)}
                />
              ))}
            </View>
          </Card>
        ) : (
          <Card>
            <EmptyState
              title="Analysis not yet run"
              subtitle="Run AI segmentation to see results"
              action={
                <Button
                  label="Analyse This Scan"
                  onPress={async () => {
                    try {
                      await api.analyze(selected.id);
                      loadData();
                    } catch {
                      Alert.alert('Error', 'Analysis failed. Check the backend is running.');
                    }
                  }}
                />
              }
            />
          </Card>
        )}

        {/* Full mandible download */}
        {isAnalysed && (
          <Card>
            <CardHeader title="Full Mandible Export" />
            <View style={{ gap: spacing.md }}>
              <Button
                label="Download Full STL"
                onPress={() => openDownload(`${BASE_URL}/stl/${selected.id}`)}
                fullWidth
              />
              <Button
                label="Download Full DICOM"
                variant="outline"
                onPress={() => openDownload(`${BASE_URL}/export-dicom/${selected.id}/full`)}
                fullWidth
              />
            </View>
          </Card>
        )}

      </ScrollView>
    </View>
  );
}

const InfoCell = ({ label, value }: { label: string; value: string }) => (
  <View style={{ width: '48%', backgroundColor: colors.bgSurface, borderWidth: 1, borderColor: colors.border, borderRadius: radius.md, padding: spacing.md, marginBottom: spacing.sm }}>
    <Text style={{ fontSize: 9, fontWeight: '700', color: colors.textMuted, textTransform: 'uppercase', letterSpacing: 0.5, marginBottom: 4 }}>{label}</Text>
    <Text style={{ fontSize: 13, fontWeight: '600', color: colors.textPrimary }}>{value}</Text>
  </View>
);

const RegionCard = ({ region, scanId, onStl, onDcm }: { region: any; scanId: number; onStl: () => void; onDcm: () => void }) => (
  <View style={[rcStyles.card, { borderColor: `${region.color}30` }]}>
    <View style={rcStyles.top}>
      <Text style={rcStyles.short}>{region.short}</Text>
    </View>
    <Text style={[rcStyles.name, { color: region.color }]}>{region.label}</Text>
    <View style={rcStyles.btns}>
      <TouchableOpacity onPress={onStl} style={[rcStyles.btn, { backgroundColor: 'rgba(59,130,246,.12)', borderColor: 'rgba(59,130,246,.3)' }]}>
        <Text style={{ fontSize: 9, fontWeight: '700', color: '#93c5fd' }}>STL</Text>
      </TouchableOpacity>
      <TouchableOpacity onPress={onDcm} style={[rcStyles.btn, { backgroundColor: 'rgba(6,182,212,.12)', borderColor: 'rgba(6,182,212,.3)' }]}>
        <Text style={{ fontSize: 9, fontWeight: '700', color: '#67e8f9' }}>DCM</Text>
      </TouchableOpacity>
    </View>
  </View>
);

const rcStyles = StyleSheet.create({
  card: { width: '47%', backgroundColor: colors.bgSurface, borderWidth: 1, borderRadius: radius.md, padding: spacing.md, margin: '1.5%', alignItems: 'center' },
  top: { width: 36, height: 36, borderRadius: 18, backgroundColor: 'rgba(59,130,246,.1)', alignItems: 'center', justifyContent: 'center', marginBottom: 8 },
  short: { fontSize: 10, fontWeight: '800', color: colors.accent },
  name: { fontSize: 11, fontWeight: '700', textAlign: 'center', marginBottom: 10 },
  btns: { flexDirection: 'row', gap: 6 },
  btn: { paddingHorizontal: 10, paddingVertical: 4, borderRadius: radius.sm, borderWidth: 1 },
});

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.bgBase },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: spacing.xl, paddingTop: 52, paddingBottom: spacing.lg, borderBottomWidth: 1, borderBottomColor: colors.border, backgroundColor: colors.bgSurface },
  title: { fontSize: 22, fontWeight: '700', color: colors.textPrimary },
  subtitle: { fontSize: 12, color: colors.textMuted, marginTop: 2 },
  scroll: { padding: spacing.lg, paddingBottom: 100 },
  scanChip: { paddingHorizontal: 16, paddingVertical: 8, backgroundColor: colors.bgCard, borderWidth: 1, borderColor: colors.border, borderRadius: radius.full },
  scanChipActive: { borderColor: colors.accent, backgroundColor: 'rgba(59,130,246,.12)' },
  scanChipText: { fontSize: 12, fontWeight: '600', color: colors.textSecondary },
  infoGrid: { flexDirection: 'row', flexWrap: 'wrap', justifyContent: 'space-between' },
  regionGrid: { flexDirection: 'row', flexWrap: 'wrap' },
});
