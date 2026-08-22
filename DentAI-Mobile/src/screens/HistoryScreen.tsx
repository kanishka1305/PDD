import React, { useState, useCallback } from 'react';
import {
  View, Text, StyleSheet, FlatList, TouchableOpacity,
  TextInput, RefreshControl, StatusBar,
} from 'react-native';
import { useFocusEffect } from '@react-navigation/native';
import { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import LinearGradient from 'react-native-linear-gradient';
import { colors, spacing, radius, typography, shadows } from '../utils/theme';
import { StatusPill, EmptyState, Skeleton } from '../components/UI';
import { api } from '../api/client';
import { MainTabParamList } from '../navigation/types';
import dayjs from 'dayjs';

type Props = { navigation: BottomTabNavigationProp<MainTabParamList, 'History'> };

const FILTERS = ['All', 'Analysed', 'Pending'] as const;
type Filter = typeof FILTERS[number];

export default function HistoryScreen({ navigation }: Props) {
  const [scans, setScans]         = useState<any[]>([]);
  const [loading, setLoading]     = useState(true);
  const [refreshing, setRefreshing] = useState(false);
  const [search, setSearch]       = useState('');
  const [filter, setFilter]       = useState<Filter>('All');

  const fetchScans = async () => {
    try {
      const res = await api.getScans();
      setScans(res.data.scans || []);
    } catch {}
    finally { setLoading(false); setRefreshing(false); }
  };

  useFocusEffect(useCallback(() => { fetchScans(); }, []));
  const onRefresh = () => { setRefreshing(true); fetchScans(); };

  const filtered = scans.filter(s => {
    const matchSearch = !search ||
      (s.patient_name || '').toLowerCase().includes(search.toLowerCase()) ||
      String(s.id).includes(search);
    const matchFilter =
      filter === 'All' ? true :
      filter === 'Analysed' ? (s.status === 'analysed' || s.status === 'analyzed') :
      s.status === 'uploaded';
    return matchSearch && matchFilter;
  });

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={colors.bgBase} />

      {/* Header */}
      <View style={styles.header}>
        <Text style={styles.title}>Scan History</Text>
        <Text style={styles.subtitle}>{scans.length} total scans</Text>
      </View>

      {/* Search */}
      <View style={styles.searchWrap}>
        <Text style={styles.searchIcon}>🔍</Text>
        <TextInput
          style={styles.searchInput}
          value={search}
          onChangeText={setSearch}
          placeholder="Search by patient or ID…"
          placeholderTextColor={colors.textMuted}
          autoCapitalize="none"
        />
        {search.length > 0 && (
          <TouchableOpacity onPress={() => setSearch('')} style={{ padding: 8 }}>
            <Text style={{ color: colors.textMuted, fontSize: 16 }}>✕</Text>
          </TouchableOpacity>
        )}
      </View>

      {/* Filter Pills */}
      <View style={styles.filterRow}>
        {FILTERS.map(f => (
          <TouchableOpacity
            key={f}
            style={[styles.pill, filter === f && styles.pillActive]}
            onPress={() => setFilter(f)}>
            <Text style={[styles.pillText, filter === f && styles.pillTextActive]}>{f}</Text>
          </TouchableOpacity>
        ))}
        <Text style={styles.resultCount}>{filtered.length} results</Text>
      </View>

      {/* List */}
      {loading ? (
        <View style={{ padding: spacing.lg }}>
          {[0,1,2,3,4].map(i => <ScanCardSkeleton key={i} />)}
        </View>
      ) : (
        <FlatList
          data={filtered}
          keyExtractor={item => String(item.id)}
          renderItem={({ item }) => (
            <ScanCard
              scan={item}
              onPress={() => navigation.navigate('Results', { scanId: item.id })}
            />
          )}
          contentContainerStyle={styles.list}
          refreshControl={<RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={colors.accent} />}
          ListEmptyComponent={
            <EmptyState
              title={search ? 'No scans match your search' : 'No scans yet'}
              subtitle={search ? 'Try a different search term' : 'Upload your first CBCT scan'}
            />
          }
          showsVerticalScrollIndicator={false}
        />
      )}
    </View>
  );
}

const ScanCard = ({ scan, onPress }: { scan: any; onPress: () => void }) => (
  <TouchableOpacity style={scStyles.card} onPress={onPress} activeOpacity={0.85}>
    <LinearGradient
      colors={['rgba(59,130,246,.2)', 'rgba(6,182,212,.15)']}
      style={scStyles.icon}>
      <Text style={{ fontSize: 22 }}>🦷</Text>
    </LinearGradient>
    <View style={{ flex: 1 }}>
      <Text style={scStyles.name} numberOfLines={1}>
        {scan.patient_name || `Scan #${scan.id}`}
      </Text>
      <Text style={scStyles.meta}>
        ID: {scan.patient_id || `SCN-${String(scan.id).padStart(4, '0')}`}
      </Text>
      <Text style={scStyles.date}>
        {scan.modality || 'CBCT'} · {dayjs(scan.created_at).format('DD MMM YYYY, HH:mm')}
      </Text>
    </View>
    <View style={{ alignItems: 'flex-end', gap: 8 }}>
      <StatusPill status={scan.status || 'uploaded'} />
      <Text style={scStyles.arrow}>›</Text>
    </View>
  </TouchableOpacity>
);

const scStyles = StyleSheet.create({
  card: { flexDirection: 'row', alignItems: 'center', backgroundColor: colors.bgCard, borderWidth: 1, borderColor: colors.border, borderRadius: radius.lg, padding: spacing.lg, marginBottom: spacing.sm, gap: spacing.md, ...shadows.sm },
  icon: { width: 48, height: 48, borderRadius: radius.md, alignItems: 'center', justifyContent: 'center' },
  name: { fontSize: 14, fontWeight: '700', color: colors.textPrimary, marginBottom: 3 },
  meta: { fontSize: 11, color: colors.textMuted, marginBottom: 2 },
  date: { fontSize: 11, color: colors.textMuted },
  arrow: { fontSize: 20, color: colors.textMuted },
});

const ScanCardSkeleton = () => (
  <View style={{ flexDirection: 'row', alignItems: 'center', backgroundColor: colors.bgCard, borderWidth: 1, borderColor: colors.border, borderRadius: radius.lg, padding: spacing.lg, marginBottom: spacing.sm, gap: spacing.md }}>
    <Skeleton width={48} height={48} style={{ borderRadius: radius.md }} />
    <View style={{ flex: 1 }}>
      <Skeleton width="60%" height={14} style={{ marginBottom: 8 }} />
      <Skeleton width="40%" height={11} style={{ marginBottom: 6 }} />
      <Skeleton width="50%" height={11} />
    </View>
  </View>
);

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.bgBase },
  header: { paddingHorizontal: spacing.xl, paddingTop: 52, paddingBottom: spacing.lg, borderBottomWidth: 1, borderBottomColor: colors.border, backgroundColor: colors.bgSurface },
  title: { fontSize: 22, fontWeight: '700', color: colors.textPrimary },
  subtitle: { fontSize: 12, color: colors.textMuted, marginTop: 2 },
  searchWrap: { flexDirection: 'row', alignItems: 'center', backgroundColor: colors.bgSurface, borderWidth: 1.5, borderColor: colors.border, borderRadius: radius.md, marginHorizontal: spacing.lg, marginTop: spacing.lg, paddingHorizontal: spacing.md },
  searchIcon: { fontSize: 14, marginRight: 8 },
  searchInput: { flex: 1, paddingVertical: 10, fontSize: 13, color: colors.textPrimary },
  filterRow: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: spacing.lg, paddingVertical: spacing.md, gap: spacing.sm },
  pill: { paddingHorizontal: 14, paddingVertical: 7, borderRadius: radius.full, borderWidth: 1.5, borderColor: colors.borderMid },
  pillActive: { backgroundColor: 'rgba(59,130,246,.12)', borderColor: colors.accent },
  pillText: { fontSize: 12, fontWeight: '600', color: colors.textSecondary },
  pillTextActive: { color: colors.accent },
  resultCount: { marginLeft: 'auto', fontSize: 11, color: colors.textMuted },
  list: { padding: spacing.lg, paddingBottom: 100 },
});
