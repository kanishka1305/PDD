import React, { useState, useEffect, useCallback } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  RefreshControl, StatusBar, Dimensions,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import { useFocusEffect } from '@react-navigation/native';
import { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import { colors, spacing, radius, typography, shadows, gradients } from '../utils/theme';
import { Card, CardHeader, Badge, StatusPill, EmptyState, Skeleton } from '../components/UI';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { MainTabParamList } from '../navigation/types';
import dayjs from 'dayjs';

type Props = { navigation: BottomTabNavigationProp<MainTabParamList, 'Dashboard'> };

const { width } = Dimensions.get('window');

export default function DashboardScreen({ navigation }: Props) {
  const { user } = useAuth();
  const [scans, setScans]         = useState<any[]>([]);
  const [loading, setLoading]     = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [health, setHealth]       = useState<'online' | 'offline'>('offline');

  const fetchData = async () => {
    try {
      const [scansRes, healthRes] = await Promise.allSettled([
        api.getScans(),
        api.health(),
      ]);
      if (scansRes.status === 'fulfilled') setScans(scansRes.value.data.scans || []);
      setHealth(healthRes.status === 'fulfilled' ? 'online' : 'offline');
    } catch { setHealth('offline'); }
    finally { setLoading(false); setRefreshing(false); }
  };

  useFocusEffect(useCallback(() => { fetchData(); }, []));

  const onRefresh = () => { setRefreshing(true); fetchData(); };

  const total     = scans.length;
  const analysed  = scans.filter(s => s.status === 'analysed' || s.status === 'analyzed').length;
  const pending   = scans.filter(s => s.status === 'uploaded').length;
  const patients  = new Set(scans.map(s => s.patient_name || s.id)).size;
  const recent    = [...scans].slice(0, 5);

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={colors.bgBase} />

      {/* ── Header ── */}
      <LinearGradient colors={['#0f1623', '#080c18']} style={styles.header}>
        <View>
          <Text style={styles.greeting}>Good day, Dr. {user?.name?.split(' ')[0] || 'Doctor'}</Text>
          <Text style={styles.greetingSub}>Clinical overview</Text>
        </View>
        <TouchableOpacity
          style={styles.avatarBtn}
          onPress={() => navigation.navigate('Profile')}>
          <LinearGradient colors={gradients.accent} style={styles.avatar}>
            <Text style={styles.avatarText}>
              {user?.name?.charAt(0).toUpperCase() || 'D'}
            </Text>
          </LinearGradient>
        </TouchableOpacity>
      </LinearGradient>

      <ScrollView
        style={{ flex: 1 }}
        contentContainerStyle={styles.scroll}
        refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.accent} />}
        showsVerticalScrollIndicator={false}>

        {/* ── KPI Grid ── */}
        <View style={styles.kpiGrid}>
          {[
            { label: 'Patients', value: loading ? '—' : String(patients), color: 'blue' as const, sub: 'unique' },
            { label: 'Total Scans', value: loading ? '—' : String(total), color: 'cyan' as const, sub: 'all time' },
            { label: 'Analysed', value: loading ? '—' : String(analysed), color: 'green' as const, sub: `${total > 0 ? Math.round(analysed / total * 100) : 0}%` },
            { label: 'Pending', value: loading ? '—' : String(pending), color: 'amber' as const, sub: 'awaiting' },
          ].map((item, i) => (
            <KpiCard key={i} {...item} loading={loading} />
          ))}
        </View>

        {/* ── Quick Actions ── */}
        <Card style={{ marginBottom: spacing.lg }}>
          <CardHeader title="Quick Actions" />
          <View style={styles.qaGrid}>
            <QuickAction
              label="Upload Scan"
              sub="Import DICOM / NIfTI"
              color={colors.accent}
              bg="rgba(59,130,246,.1)"
              icon="⬆"
              onPress={() => navigation.navigate('Upload')}
            />
            <QuickAction
              label="View History"
              sub="Browse all scans"
              color={colors.accent2}
              bg="rgba(6,182,212,.1)"
              icon="🕐"
              onPress={() => navigation.navigate('History')}
            />
            <QuickAction
              label="Open Results"
              sub="Latest report"
              color={colors.success}
              bg="rgba(34,197,94,.1)"
              icon="📊"
              onPress={() => navigation.navigate('Results', {})}
            />
          </View>
        </Card>

        {/* ── Recent Scans ── */}
        <Card>
          <CardHeader
            title="Recent Activity"
            action={
              <TouchableOpacity onPress={() => navigation.navigate('History')}>
                <Text style={{ fontSize: 11, color: colors.accent, fontWeight: '600' }}>View all →</Text>
              </TouchableOpacity>
            }
          />
          {loading ? (
            [0, 1, 2].map(i => <ScanSkeleton key={i} />)
          ) : recent.length === 0 ? (
            <EmptyState
              title="No scans yet"
              subtitle="Upload your first CBCT scan to get started"
            />
          ) : (
            recent.map(scan => (
              <ScanRow
                key={scan.id}
                scan={scan}
                onPress={() => navigation.navigate('Results', { scanId: scan.id })}
              />
            ))
          )}
        </Card>

        {/* ── System Status ── */}
        <Card>
          <CardHeader title="System Status" />
          <SystemRow label="Backend API" detail="FastAPI / Python" status={health} />
          <SystemRow label="AI Model" detail="UNet-CBCT v2.1" status={health === 'online' ? 'online' : 'offline'} />
          <SystemRow label="Database" detail="MySQL / Local" status={health === 'online' ? 'online' : 'offline'} />
        </Card>

      </ScrollView>
    </View>
  );
}

/* ── Sub-components ── */
const KpiCard = ({ label, value, color, sub, loading }: any) => {
  const colorMap: Record<string, string> = {
    blue: colors.accent, cyan: colors.accent2,
    green: colors.success, amber: colors.warning,
  };
  const bgMap: Record<string, string> = {
    blue: 'rgba(59,130,246,.1)', cyan: 'rgba(6,182,212,.1)',
    green: 'rgba(34,197,94,.1)', amber: 'rgba(245,158,11,.1)',
  };
  return (
    <View style={kpiStyles.card}>
      <View style={[kpiStyles.dot, { backgroundColor: bgMap[color] }]}>
        <View style={{ width: 8, height: 8, borderRadius: 4, backgroundColor: colorMap[color] }} />
      </View>
      {loading ? <Skeleton width={48} height={32} style={{ marginBottom: 4 }} /> :
        <Text style={[kpiStyles.value, { color: colorMap[color] }]}>{value}</Text>
      }
      <Text style={kpiStyles.label}>{label}</Text>
      {sub && <Text style={kpiStyles.sub}>{sub}</Text>}
    </View>
  );
};

const kpiStyles = StyleSheet.create({
  card: { flex: 1, backgroundColor: colors.bgCard, borderWidth: 1, borderColor: colors.border, borderRadius: radius.lg, padding: spacing.md, margin: 4, minWidth: (width - 60) / 2 },
  dot: { width: 34, height: 34, borderRadius: radius.md, alignItems: 'center', justifyContent: 'center', marginBottom: spacing.md },
  value: { fontSize: 26, fontWeight: '800', lineHeight: 30, marginBottom: 2 },
  label: { fontSize: 10, fontWeight: '700', color: colors.textMuted, textTransform: 'uppercase', letterSpacing: 0.6 },
  sub: { fontSize: 10, color: colors.textMuted, marginTop: 2 },
});

const QuickAction = ({ label, sub, color, bg, icon, onPress }: any) => (
  <TouchableOpacity style={[qaStyles.card, { borderColor: `${color}30` }]} onPress={onPress} activeOpacity={0.8}>
    <View style={[qaStyles.icon, { backgroundColor: bg }]}>
      <Text style={{ fontSize: 22 }}>{icon}</Text>
    </View>
    <Text style={[qaStyles.label, { color }]}>{label}</Text>
    <Text style={qaStyles.sub}>{sub}</Text>
  </TouchableOpacity>
);

const qaStyles = StyleSheet.create({
  card: { flex: 1, backgroundColor: colors.bgSurface, borderWidth: 1, borderRadius: radius.md, padding: spacing.md, margin: 4, alignItems: 'center' },
  icon: { width: 44, height: 44, borderRadius: 12, alignItems: 'center', justifyContent: 'center', marginBottom: spacing.sm },
  label: { fontSize: 12, fontWeight: '700', textAlign: 'center', marginBottom: 2 },
  sub: { fontSize: 10, color: colors.textMuted, textAlign: 'center' },
});

const ScanRow = ({ scan, onPress }: { scan: any; onPress: () => void }) => (
  <TouchableOpacity style={srStyles.row} onPress={onPress} activeOpacity={0.8}>
    <LinearGradient colors={['rgba(59,130,246,.2)', 'rgba(6,182,212,.2)']} style={srStyles.icon}>
      <Text style={{ fontSize: 16 }}>🦷</Text>
    </LinearGradient>
    <View style={{ flex: 1 }}>
      <Text style={srStyles.name} numberOfLines={1}>
        {scan.patient_name || `Scan #${scan.id}`}
      </Text>
      <Text style={srStyles.meta}>
        {scan.modality || 'CBCT'} · {dayjs(scan.created_at).format('DD MMM YYYY')}
      </Text>
    </View>
    <StatusPill status={scan.status || 'uploaded'} />
  </TouchableOpacity>
);

const srStyles = StyleSheet.create({
  row: { flexDirection: 'row', alignItems: 'center', gap: spacing.md, paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: 'rgba(30,45,64,.5)' },
  icon: { width: 40, height: 40, borderRadius: radius.md, alignItems: 'center', justifyContent: 'center' },
  name: { fontSize: 13, fontWeight: '600', color: colors.textPrimary, marginBottom: 2 },
  meta: { fontSize: 11, color: colors.textMuted },
});

const ScanSkeleton = () => (
  <View style={{ flexDirection: 'row', alignItems: 'center', gap: 12, paddingVertical: 10 }}>
    <Skeleton width={40} height={40} style={{ borderRadius: radius.md }} />
    <View style={{ flex: 1 }}>
      <Skeleton width="70%" height={13} style={{ marginBottom: 6 }} />
      <Skeleton width="45%" height={11} />
    </View>
  </View>
);

const SystemRow = ({ label, detail, status }: { label: string; detail: string; status: 'online' | 'offline' }) => (
  <View style={{ flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: 'rgba(30,45,64,.5)' }}>
    <View>
      <Text style={{ fontSize: 13, fontWeight: '500', color: colors.textPrimary }}>{label}</Text>
      <Text style={{ fontSize: 11, color: colors.textMuted }}>{detail}</Text>
    </View>
    <StatusPill status={status} />
  </View>
);

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.bgBase },
  header: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingHorizontal: spacing.xl, paddingTop: 52, paddingBottom: spacing.xl, borderBottomWidth: 1, borderBottomColor: colors.border },
  greeting: { fontSize: 20, fontWeight: '700', color: colors.textPrimary },
  greetingSub: { fontSize: 12, color: colors.textMuted, marginTop: 2 },
  avatarBtn: { ...shadows.glow },
  avatar: { width: 40, height: 40, borderRadius: 20, alignItems: 'center', justifyContent: 'center' },
  avatarText: { fontSize: 16, fontWeight: '800', color: '#fff' },
  scroll: { padding: spacing.lg, paddingBottom: 100 },
  kpiGrid: { flexDirection: 'row', flexWrap: 'wrap', marginHorizontal: -4, marginBottom: spacing.sm },
  qaGrid: { flexDirection: 'row', marginHorizontal: -4 },
});
