import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  KeyboardAvoidingView, Platform, StatusBar,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { colors, spacing, radius, typography, shadows } from '../utils/theme';
import { Input, Button, Divider } from '../components/UI';
import { api } from '../api/client';
import { RootStackParamList } from '../navigation/types';

type Props = { navigation: NativeStackNavigationProp<RootStackParamList, 'Signup'> };

export default function SignupScreen({ navigation }: Props) {
  const [name, setName]         = useState('');
  const [license, setLicense]   = useState('');
  const [email, setEmail]       = useState('');
  const [password, setPassword] = useState('');
  const [showPw, setShowPw]     = useState(false);
  const [loading, setLoading]   = useState(false);
  const [error, setError]       = useState('');
  const [success, setSuccess]   = useState('');

  const pwStrength = () => {
    if (!password) return { score: 0, label: '', color: colors.border };
    const checks = [
      password.length >= 8,
      /[A-Z]/.test(password),
      /[a-z]/.test(password),
      /\d/.test(password),
      /[@#$%^&+=!]/.test(password),
    ];
    const score = checks.filter(Boolean).length;
    const labels = ['', 'Very Weak', 'Weak', 'Fair', 'Strong', 'Very Strong'];
    const clrs   = ['', '#ef4444', '#f97316', '#eab308', '#22c55e', '#3b82f6'];
    return { score, label: labels[score], color: clrs[score] };
  };

  const pw = pwStrength();

  const handleSignup = async () => {
    if (!name.trim() || !license.trim() || !email.trim() || !password) {
      setError('All fields are required.'); return;
    }
    if (password.length < 8) {
      setError('Password must be at least 8 characters.'); return;
    }
    setLoading(true); setError('');
    try {
      const res = await api.signup(name.trim(), license.trim(), email.trim().toLowerCase(), password);
      if (res.data.success) {
        setSuccess('Account created! Redirecting to login…');
        setTimeout(() => navigation.navigate('Login'), 1500);
      } else {
        setError(res.data.message || 'Signup failed. Please try again.');
      }
    } catch {
      setError('Cannot reach server. Make sure the backend is running.');
    } finally { setLoading(false); }
  };

  return (
    <LinearGradient colors={['#080c18', '#0f1623']} style={styles.bg}>
      <StatusBar barStyle="light-content" backgroundColor="#080c18" />
      <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled" showsVerticalScrollIndicator={false}>
          <View style={styles.logoWrap}>
            <LinearGradient colors={['#3b82f6', '#06b6d4']} style={styles.logoMark}>
              <Text style={{ fontSize: 26, color: '#fff' }}>⬡</Text>
            </LinearGradient>
            <Text style={styles.brandName}>DentAI</Text>
            <Text style={styles.brandSub}>CBCT AI Segmentation Platform</Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.heading}>Create your account</Text>
            <Text style={styles.subheading}>Join the platform — clinical access only</Text>

            {!!error && (
              <View style={styles.alertError}>
                <Text style={{ fontSize: 13, color: '#fca5a5' }}>{error}</Text>
              </View>
            )}
            {!!success && (
              <View style={styles.alertSuccess}>
                <Text style={{ fontSize: 13, color: '#86efac' }}>{success}</Text>
              </View>
            )}

            <Input label="Full Name" value={name} onChangeText={setName}
              placeholder="Dr. Jane Smith" autoCapitalize="words" />
            <Input label="License Number" value={license} onChangeText={setLicense}
              placeholder="MED-123456" autoCapitalize="characters" />
            <Input label="Email address" value={email} onChangeText={setEmail}
              placeholder="doctor@hospital.com" keyboardType="email-address" autoCapitalize="none" />
            <Input label="Password" value={password} onChangeText={setPassword}
              placeholder="Min 8 chars" secureTextEntry={!showPw}
              rightIcon={
                <TouchableOpacity onPress={() => setShowPw(!showPw)}>
                  <Text style={{ fontSize: 16, color: colors.textMuted }}>{showPw ? '🙈' : '👁️'}</Text>
                </TouchableOpacity>
              }
            />

            {/* Password strength bar */}
            {password.length > 0 && (
              <View style={{ marginTop: -spacing.sm, marginBottom: spacing.lg }}>
                <View style={styles.pwBarBg}>
                  <View style={[styles.pwBarFill, { width: `${pw.score / 5 * 100}%` as any, backgroundColor: pw.color }]} />
                </View>
                <Text style={{ fontSize: 11, color: pw.color, marginTop: 4 }}>{pw.label}</Text>
              </View>
            )}

            <Button onPress={handleSignup} label="Create Account" loading={loading} fullWidth />
            <Divider label="or" />
            <View style={{ flexDirection: 'row', justifyContent: 'center' }}>
              <Text style={{ fontSize: 13, color: colors.textSecondary }}>Already have an account? </Text>
              <TouchableOpacity onPress={() => navigation.navigate('Login')}>
                <Text style={{ fontSize: 13, color: colors.accent, fontWeight: '500' }}>Sign in</Text>
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  bg: { flex: 1 },
  scroll: { flexGrow: 1, alignItems: 'center', justifyContent: 'center', padding: spacing.xl },
  logoWrap: { alignItems: 'center', marginBottom: spacing.xxxl },
  logoMark: { width: 56, height: 56, borderRadius: 14, alignItems: 'center', justifyContent: 'center', marginBottom: 12 },
  brandName: { fontSize: 28, fontWeight: '800', color: colors.accent, letterSpacing: -0.5 },
  brandSub: { fontSize: 13, color: colors.textMuted, marginTop: 4 },
  card: { width: '100%', backgroundColor: colors.bgCard, borderWidth: 1, borderColor: colors.border, borderRadius: radius.xl, padding: spacing.xxl, ...shadows.lg },
  heading: { fontSize: 20, fontWeight: '700', color: colors.textPrimary, marginBottom: 4 },
  subheading: { fontSize: 13, color: colors.textSecondary, marginBottom: spacing.xxl },
  alertError: { backgroundColor: 'rgba(239,68,68,.1)', borderWidth: 1, borderColor: 'rgba(239,68,68,.4)', borderRadius: radius.md, padding: spacing.md, marginBottom: spacing.lg },
  alertSuccess: { backgroundColor: 'rgba(34,197,94,.1)', borderWidth: 1, borderColor: 'rgba(34,197,94,.4)', borderRadius: radius.md, padding: spacing.md, marginBottom: spacing.lg },
  pwBarBg: { height: 3, borderRadius: 2, backgroundColor: colors.border, overflow: 'hidden' },
  pwBarFill: { height: 3, borderRadius: 2 },
});
