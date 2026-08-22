import React, { useState } from 'react';
import {
  View, Text, StyleSheet, ScrollView, TouchableOpacity,
  KeyboardAvoidingView, Platform, StatusBar,
} from 'react-native';
import LinearGradient from 'react-native-linear-gradient';
import { NativeStackNavigationProp } from '@react-navigation/native-stack';
import { colors, spacing, radius, typography, shadows } from '../utils/theme';
import { Input, Button } from '../components/UI';
import { api } from '../api/client';
import { RootStackParamList } from '../navigation/types';

type Props = { navigation: NativeStackNavigationProp<RootStackParamList, 'ForgotPassword'> };

export default function ForgotPasswordScreen({ navigation }: Props) {
  const [email, setEmail]     = useState('');
  const [loading, setLoading] = useState(false);
  const [error, setError]     = useState('');
  const [success, setSuccess] = useState('');

  const handleSubmit = async () => {
    if (!email.trim()) { setError('Please enter your email address.'); return; }
    setLoading(true); setError('');
    try {
      const res = await api.forgotPassword(email.trim().toLowerCase());
      if (res.data.success) {
        setSuccess(res.data.message || 'If that email is registered, a reset link has been sent.');
      } else {
        setError(res.data.message || 'Something went wrong. Please try again.');
      }
    } catch {
      setError('Cannot reach server. Make sure the backend is running.');
    } finally { setLoading(false); }
  };

  return (
    <LinearGradient colors={['#080c18', '#0f1623']} style={{ flex: 1 }}>
      <StatusBar barStyle="light-content" backgroundColor="#080c18" />
      <KeyboardAvoidingView style={{ flex: 1 }} behavior={Platform.OS === 'ios' ? 'padding' : undefined}>
        <ScrollView contentContainerStyle={styles.scroll} keyboardShouldPersistTaps="handled">
          <View style={styles.logoWrap}>
            <LinearGradient colors={['#3b82f6', '#06b6d4']} style={styles.logoMark}>
              <Text style={{ fontSize: 26, color: '#fff' }}>⬡</Text>
            </LinearGradient>
            <Text style={styles.brandName}>DentAI</Text>
          </View>

          <View style={styles.card}>
            <Text style={styles.heading}>Forgot Password</Text>
            <Text style={styles.subheading}>
              Enter your registered email and we'll send a reset link
            </Text>

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

            <Input
              label="Email address"
              value={email}
              onChangeText={setEmail}
              placeholder="doctor@hospital.com"
              keyboardType="email-address"
              autoCapitalize="none"
              editable={!success}
            />

            {!success && (
              <Button onPress={handleSubmit} label="Send Reset Link" loading={loading} fullWidth style={{ marginTop: spacing.sm }} />
            )}

            <TouchableOpacity
              onPress={() => navigation.navigate('Login')}
              style={styles.backBtn}>
              <Text style={styles.backText}>← Back to Login</Text>
            </TouchableOpacity>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </LinearGradient>
  );
}

const styles = StyleSheet.create({
  scroll: { flexGrow: 1, alignItems: 'center', justifyContent: 'center', padding: spacing.xl },
  logoWrap: { alignItems: 'center', marginBottom: spacing.xxxl },
  logoMark: { width: 56, height: 56, borderRadius: 14, alignItems: 'center', justifyContent: 'center', marginBottom: 12 },
  brandName: { fontSize: 28, fontWeight: '800', color: colors.accent },
  card: { width: '100%', backgroundColor: colors.bgCard, borderWidth: 1, borderColor: colors.border, borderRadius: radius.xl, padding: spacing.xxl, ...shadows.lg },
  heading: { fontSize: 20, fontWeight: '700', color: colors.textPrimary, marginBottom: 4 },
  subheading: { fontSize: 13, color: colors.textSecondary, marginBottom: spacing.xxl },
  alertError: { backgroundColor: 'rgba(239,68,68,.1)', borderWidth: 1, borderColor: 'rgba(239,68,68,.4)', borderRadius: radius.md, padding: spacing.md, marginBottom: spacing.lg },
  alertSuccess: { backgroundColor: 'rgba(34,197,94,.1)', borderWidth: 1, borderColor: 'rgba(34,197,94,.4)', borderRadius: radius.md, padding: spacing.md, marginBottom: spacing.lg },
  backBtn: { alignItems: 'center', marginTop: spacing.xl },
  backText: { fontSize: 13, color: colors.accent, fontWeight: '500' },
});
