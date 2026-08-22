// ═══════════════════════════════════════════════════════════
// DentAI Mobile — Login Screen
// Matches web login.html design exactly
// ═══════════════════════════════════════════════════════════
import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  KeyboardAvoidingView, Platform, Alert, StatusBar,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { colors, spacing, radius, typography, shadows } from '../utils/theme';
import { Input, Button, Divider } from '../components/UI';
import { api } from '../api/client';
import { useAuth } from '../context/AuthContext';
import { RootStackParamList } from '../navigation/types';

type Props = { navigation: NativeStackNavigationProp<RootStackParamList, 'Login'> };

export default function LoginScreen({ navigation }: Props) {
  const { login } = useAuth();
  const [email, setEmail] = useState('');
  const [password, setPassword] = useState('');
  const [showPw, setShowPw] = useState(false);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleLogin = async () => {
    if (!email.trim() || !password) {
      setError('Please enter your email and password.');
      return;
    }
    setLoading(true);
    setError('');
    try {
      const res = await api.login(email.trim().toLowerCase(), password);
      const data = res.data;
      if (data.success) {
        await login(
          { id: data.id, name: data.name, email: data.email },
          data.access_token,
        );
      } else {
        setError(data.message || 'Invalid email or password.');
      }
    } catch (err: any) {
      setError('Cannot reach server. Make sure the backend is running.');
    } finally {
      setLoading(false);
    }
  };

  return (
    <LinearGradient
      colors={['#080c18', '#0f1623']}
      style={styles.bg}>
      <StatusBar barStyle="light-content" backgroundColor="#080c18" />
      <KeyboardAvoidingView
        style={{ flex: 1 }}
        behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <ScrollView
          contentContainerStyle={styles.scroll}
          keyboardShouldPersistTaps="handled"
          showsVerticalScrollIndicator={false}>

          {/* ── Brand ── */}
          <View style={styles.logoWrap}>
            <LinearGradient
              colors={['#3b82f6', '#06b6d4']}
              style={styles.logoMark}>
              <Text style={styles.logoIcon}>⬡</Text>
            </LinearGradient>
            <Text style={styles.brandName}>DentAI</Text>
            <Text style={styles.brandSub}>CBCT AI Segmentation Platform</Text>
          </View>

          {/* ── Card ── */}
          <View style={styles.card}>
            <Text style={styles.heading}>Welcome back</Text>
            <Text style={styles.subheading}>Sign in to your clinical account</Text>

            {/* Error alert */}
            {!!error && (
              <View style={styles.alertError}>
                <Text style={styles.alertText}>{error}</Text>
              </View>
            )}

            <Input
              label="Email address"
              value={email}
              onChangeText={setEmail}
              placeholder="doctor@hospital.com"
              keyboardType="email-address"
              autoCapitalize="none"
              autoCorrect={false}
              textContentType="emailAddress"
            />

            <Input
              label="Password"
              value={password}
              onChangeText={setPassword}
              placeholder="••••••••"
              secureTextEntry={!showPw}
              textContentType="password"
              rightIcon={
                <TouchableOpacity onPress={() => setShowPw(!showPw)}>
                  <Text style={styles.eyeBtn}>{showPw ? '🙈' : '👁️'}</Text>
                </TouchableOpacity>
              }
            />

            <TouchableOpacity
              onPress={() => navigation.navigate('ForgotPassword')}
              style={styles.forgotWrap}>
              <Text style={styles.forgotLink}>Forgot password?</Text>
            </TouchableOpacity>

            <Button
              onPress={handleLogin}
              label="Sign In"
              loading={loading}
              fullWidth
              style={{ marginTop: spacing.sm }}
            />

            <Divider label="or" />

            <View style={styles.footer}>
              <Text style={styles.footerText}>Don't have an account? </Text>
              <TouchableOpacity onPress={() => navigation.navigate('Signup')}>
                <Text style={styles.footerLink}>Create account</Text>
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
  scroll: {
    flexGrow: 1,
    alignItems: 'center',
    justifyContent: 'center',
    padding: spacing.xl,
  },
  logoWrap: {
    alignItems: 'center',
    marginBottom: spacing.xxxl,
  },
  logoMark: {
    width: 56,
    height: 56,
    borderRadius: 14,
    alignItems: 'center',
    justifyContent: 'center',
    marginBottom: spacing.md,
    ...shadows.glow,
  },
  logoIcon: { fontSize: 26, color: '#fff' },
  brandName: {
    fontSize: typography.sizes.xxxl,
    fontWeight: typography.weights.extrabold,
    color: colors.accent,
    letterSpacing: -0.5,
  },
  brandSub: {
    fontSize: typography.sizes.base,
    color: colors.textMuted,
    marginTop: 4,
  },
  card: {
    width: '100%',
    backgroundColor: colors.bgCard,
    borderWidth: 1,
    borderColor: colors.border,
    borderRadius: radius.xl,
    padding: spacing.xxl,
    ...shadows.lg,
  },
  heading: {
    fontSize: typography.sizes.xl,
    fontWeight: typography.weights.bold,
    color: colors.textPrimary,
    marginBottom: 4,
  },
  subheading: {
    fontSize: typography.sizes.base,
    color: colors.textSecondary,
    marginBottom: spacing.xxl,
  },
  alertError: {
    backgroundColor: 'rgba(239,68,68,.1)',
    borderWidth: 1,
    borderColor: 'rgba(239,68,68,.4)',
    borderRadius: radius.md,
    padding: spacing.md,
    marginBottom: spacing.lg,
  },
  alertText: {
    fontSize: typography.sizes.base,
    color: '#fca5a5',
  },
  forgotWrap: { alignSelf: 'flex-end', marginTop: -spacing.sm, marginBottom: spacing.md },
  forgotLink: {
    fontSize: typography.sizes.sm,
    color: colors.accent,
    fontWeight: typography.weights.medium,
  },
  eyeBtn: { fontSize: 16, color: colors.textMuted },
  footer: { flexDirection: 'row', justifyContent: 'center' },
  footerText: { fontSize: typography.sizes.base, color: colors.textSecondary },
  footerLink: {
    fontSize: typography.sizes.base,
    color: colors.accent,
    fontWeight: typography.weights.medium,
  },
});
