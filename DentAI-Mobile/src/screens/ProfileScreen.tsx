import React, { useState, useEffect } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  Alert, StatusBar,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import { BottomTabNavigationProp } from '@react-navigation/bottom-tabs';
import { colors, spacing, radius, shadows, gradients } from '../utils/theme';
import { Card, CardHeader, Input, Button } from '../components/UI';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { MainTabParamList } from '../navigation/types';

type Props = { navigation: BottomTabNavigationProp<MainTabParamList, 'Profile'> };

export default function ProfileScreen({ navigation }: Props) {
  const { user, logout } = useAuth();
  const [profile, setProfile]   = useState<any>(null);
  const [loading, setLoading]   = useState(true);
  const [saving, setSaving]     = useState(false);
  const [name, setName]         = useState('');
  const [phone, setPhone]       = useState('');
  const [clinic, setClinic]     = useState('');
  const [success, setSuccess]   = useState('');
  const [error, setError]       = useState('');

  useEffect(() => { loadProfile(); }, []);

  const loadProfile = async () => {
    if (!user?.id) return;
    try {
      const res = await api.fetchProfile(user.id);
      const d = res.data.data;
      setProfile(d);
      setName(d.name || '');
      setPhone(d.phone || '');
      setClinic(d.clinic || '');
    } catch {}
    finally { setLoading(false); }
  };

  const handleSave = async () => {
    if (!user?.id) return;
    setSaving(true); setError(''); setSuccess('');
    try {
      const res = await api.updateProfile(user.id, {
        name, phone, clinic, email: user.email,
      });
      if (res.data.success) {
        setSuccess('Profile updated successfully!');
        loadProfile();
      } else {
        setError(res.data.message || 'Update failed.');
      }
    } catch {
      setError('Cannot reach server.');
    } finally { setSaving(false); }
  };

  const handleLogout = () => {
    Alert.alert('Sign Out', 'Are you sure you want to sign out?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Sign Out', style: 'destructive', onPress: logout },
    ]);
  };

  return (
    <View style={styles.container}>
      <StatusBar barStyle="light-content" backgroundColor={colors.bgBase} />

      {/* Header */}
      <LinearGradient colors={['#0f1623', '#080c18']} style={styles.header}>
        <LinearGradient colors={gradients.accent} style={styles.avatar}>
          <Text style={styles.avatarText}>
            {user?.name?.charAt(0).toUpperCase() || 'D'}
          </Text>
        </LinearGradient>
        <View style={{ flex: 1, marginLeft: spacing.lg }}>
          <Text style={styles.userName}>Dr. {user?.name}</Text>
          <Text style={styles.userEmail}>{user?.email}</Text>
        </View>
      </LinearGradient>

      <ScrollView contentContainerStyle={styles.scroll} showsVerticalScrollIndicator={false}>

        {!!error && (
          <View style={styles.alertError}>
            <Text style={{ color: '#fca5a5', fontSize: 13 }}>{error}</Text>
          </View>
        )}
        {!!success && (
          <View style={styles.alertSuccess}>
            <Text style={{ color: '#86efac', fontSize: 13 }}>{success}</Text>
          </View>
        )}

        {/* Profile Form */}
        <Card>
          <CardHeader title="Personal Information" />
          <Input label="Full Name" value={name} onChangeText={setName}
            placeholder="Dr. Jane Smith" autoCapitalize="words" />
          <Input label="Email Address" value={user?.email || ''} editable={false}
            containerStyle={{ opacity: 0.6 }} />
          <Input label="Phone Number" value={phone} onChangeText={setPhone}
            placeholder="+1 234 567 8900" keyboardType="phone-pad" />
          <Input label="Clinic / Hospital" value={clinic} onChangeText={setClinic}
            placeholder="City Medical Centre" />
          <Button onPress={handleSave} label="Save Changes" loading={saving} fullWidth />
        </Card>

        {/* Security */}
        <Card>
          <CardHeader title="Security" />
          <TouchableOpacity
            style={styles.menuItem}
            onPress={() => Alert.alert('Change Password', 'Navigate to change password screen')}>
            <Text style={styles.menuLabel}>🔒  Change Password</Text>
            <Text style={styles.menuArrow}>›</Text>
          </TouchableOpacity>
          <TouchableOpacity style={styles.menuItem}
            onPress={() => Alert.alert('Credentials', 'Navigate to credentials screen')}>
            <Text style={styles.menuLabel}>🎓  My Credentials</Text>
            <Text style={styles.menuArrow}>›</Text>
          </TouchableOpacity>
        </Card>

        {/* App Info */}
        <Card>
          <CardHeader title="About" />
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Version</Text>
            <Text style={styles.infoValue}>1.0.0</Text>
          </View>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>Backend</Text>
            <Text style={styles.infoValue}>FastAPI 2.0 · Local</Text>
          </View>
          <View style={styles.infoRow}>
            <Text style={styles.infoLabel}>AI Model</Text>
            <Text style={styles.infoValue}>UNet-CBCT v2.1</Text>
          </View>
        </Card>

        {/* Sign Out */}
        <Button
          onPress={handleLogout}
          label="Sign Out"
          variant="danger"
          fullWidth
          style={{ marginBottom: spacing.xxxl }}
        />

      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: colors.bgBase },
  header: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: spacing.xl, paddingTop: 52, paddingBottom: spacing.xl, borderBottomWidth: 1, borderBottomColor: colors.border },
  avatar: { width: 56, height: 56, borderRadius: 28, alignItems: 'center', justifyContent: 'center', ...shadows.glow },
  avatarText: { fontSize: 22, fontWeight: '800', color: '#fff' },
  userName: { fontSize: 18, fontWeight: '700', color: colors.textPrimary, marginBottom: 2 },
  userEmail: { fontSize: 12, color: colors.textMuted },
  scroll: { padding: spacing.lg, paddingBottom: 100 },
  alertError: { backgroundColor: 'rgba(239,68,68,.1)', borderWidth: 1, borderColor: 'rgba(239,68,68,.4)', borderRadius: radius.md, padding: spacing.md, marginBottom: spacing.lg },
  alertSuccess: { backgroundColor: 'rgba(34,197,94,.1)', borderWidth: 1, borderColor: 'rgba(34,197,94,.4)', borderRadius: radius.md, padding: spacing.md, marginBottom: spacing.lg },
  menuItem: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingVertical: 13, borderBottomWidth: 1, borderBottomColor: 'rgba(30,45,64,.5)' },
  menuLabel: { fontSize: 13, color: colors.textSecondary },
  menuArrow: { fontSize: 20, color: colors.textMuted },
  infoRow: { flexDirection: 'row', justifyContent: 'space-between', paddingVertical: 10, borderBottomWidth: 1, borderBottomColor: 'rgba(30,45,64,.5)' },
  infoLabel: { fontSize: 13, color: colors.textSecondary },
  infoValue: { fontSize: 13, fontWeight: '600', color: colors.textPrimary },
});
