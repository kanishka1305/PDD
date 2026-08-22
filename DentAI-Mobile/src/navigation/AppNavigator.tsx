// ═══════════════════════════════════════════════════════════
// DentAI Mobile — Root Navigator
// ═══════════════════════════════════════════════════════════
import React from 'react';
import { View, ActivityIndicator } from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import LinearGradient from 'react-native-linear-gradient';

import { useAuth } from '../context/AuthContext';
import { colors, spacing } from '../utils/theme';
import { RootStackParamList, MainTabParamList } from './types';

// Screens
import LoginScreen         from '../screens/LoginScreen';
import SignupScreen        from '../screens/SignupScreen';
import ForgotPasswordScreen from '../screens/ForgotPasswordScreen';
import DashboardScreen     from '../screens/DashboardScreen';
import UploadScreen        from '../screens/UploadScreen';
import HistoryScreen       from '../screens/HistoryScreen';
import ResultsScreen       from '../screens/ResultsScreen';
import ProfileScreen       from '../screens/ProfileScreen';

const Stack = createNativeStackNavigator<RootStackParamList>();
const Tab   = createBottomTabNavigator<MainTabParamList>();

// ── Tab Icon ──────────────────────────────────────────────
const TabIcon = ({ emoji, label, focused }: { emoji: string; label: string; focused: boolean }) => (
  <View style={{ alignItems: 'center', gap: 3 }}>
    <View style={{
      width: 40, height: 40, borderRadius: 20,
      alignItems: 'center', justifyContent: 'center',
      backgroundColor: focused ? 'rgba(59,130,246,.15)' : 'transparent',
    }}>
      <View style={{ opacity: focused ? 1 : 0.6 }}>
        <View style={{ fontSize: 20 } as any}>
          {/* Use text emoji as icon placeholder */}
        </View>
      </View>
    </View>
  </View>
);

// ── Main Tab Navigator ────────────────────────────────────
function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown: false,
        tabBarStyle: {
          backgroundColor: colors.bgCard,
          borderTopColor: colors.border,
          borderTopWidth: 1,
          height: 64,
          paddingBottom: 8,
          paddingTop: 6,
        },
        tabBarActiveTintColor: colors.accent,
        tabBarInactiveTintColor: colors.textMuted,
        tabBarLabelStyle: {
          fontSize: 10,
          fontWeight: '600',
          letterSpacing: 0.2,
        },
      }}>
      <Tab.Screen
        name="Dashboard"
        component={DashboardScreen}
        options={{ tabBarLabel: 'Home', tabBarIcon: ({ focused }) => <TabIcon emoji="🏠" label="Home" focused={focused} /> }}
      />
      <Tab.Screen
        name="Upload"
        component={UploadScreen}
        options={{
          tabBarLabel: 'Upload',
          tabBarIcon: ({ focused }) => (
            <View style={{
              width: 48, height: 48, borderRadius: 24, marginBottom: 4,
              backgroundColor: focused ? colors.accent : 'rgba(59,130,246,.2)',
              alignItems: 'center', justifyContent: 'center',
              shadowColor: colors.accent, shadowOffset: { width: 0, height: 3 },
              shadowOpacity: 0.4, shadowRadius: 8, elevation: 6,
            }}>
              <View style={{ width: 18, height: 18, borderRadius: 2, borderWidth: 2, borderColor: '#fff', alignItems: 'center', justifyContent: 'center' }}>
                <View style={{ width: 2, height: 8, backgroundColor: '#fff', position: 'absolute' }} />
                <View style={{ width: 8, height: 2, backgroundColor: '#fff', position: 'absolute' }} />
              </View>
            </View>
          ),
          tabBarIconStyle: { marginTop: -8 },
        }}
      />
      <Tab.Screen
        name="History"
        component={HistoryScreen}
        options={{ tabBarLabel: 'History', tabBarIcon: ({ focused }) => <TabIcon emoji="🕐" label="History" focused={focused} /> }}
      />
      <Tab.Screen
        name="Results"
        component={ResultsScreen}
        options={{ tabBarLabel: 'Results', tabBarIcon: ({ focused }) => <TabIcon emoji="📊" label="Results" focused={focused} /> }}
      />
      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{ tabBarLabel: 'Profile', tabBarIcon: ({ focused }) => <TabIcon emoji="👤" label="Profile" focused={focused} /> }}
      />
    </Tab.Navigator>
  );
}

// ── Root Stack ────────────────────────────────────────────
export default function AppNavigator() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <View style={{ flex: 1, backgroundColor: colors.bgBase, alignItems: 'center', justifyContent: 'center' }}>
        <ActivityIndicator color={colors.accent} size="large" />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <Stack.Navigator screenOptions={{ headerShown: false, animation: 'fade' }}>
        {isAuthenticated ? (
          <Stack.Screen name="Main" component={MainTabs} />
        ) : (
          <>
            <Stack.Screen name="Login"           component={LoginScreen} />
            <Stack.Screen name="Signup"          component={SignupScreen} />
            <Stack.Screen name="ForgotPassword"  component={ForgotPasswordScreen} />
          </>
        )}
      </Stack.Navigator>
    </NavigationContainer>
  );
}
