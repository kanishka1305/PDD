/**
 * DentAI Mobile — Root Navigator
 * Same backend as web app. UI/UX redesigned for mobile.
 *
 * Tab icons use react-native-vector-icons/MaterialCommunityIcons.
 * If vector-icons is not linked, falls back to clean text/emoji icons.
 */
import React from 'react';
import {
  View, Text, ActivityIndicator, StyleSheet, Platform,
} from 'react-native';
import { NavigationContainer } from '@react-navigation/native';
import { createNativeStackNavigator } from '@react-navigation/native-stack';
import { createBottomTabNavigator } from '@react-navigation/bottom-tabs';
import LinearGradient from 'react-native-linear-gradient';

import { useAuth } from '../context/AuthContext';
import { colors, spacing, radius, shadows, typography } from '../utils/theme';
import {
  RootStackParamList,
  MainTabParamList,
  MainStackParamList,
} from './types';

// ── Screens ───────────────────────────────────────────────
import LoginScreen          from '../screens/LoginScreen';
import SignupScreen         from '../screens/SignupScreen';
import ForgotPasswordScreen from '../screens/ForgotPasswordScreen';
import DashboardScreen      from '../screens/DashboardScreen';
import UploadScreen         from '../screens/UploadScreen';
import HistoryScreen        from '../screens/HistoryScreen';
import ResultsScreen        from '../screens/ResultsScreen';
import ProfileScreen        from '../screens/ProfileScreen';
import WorkflowScreen       from '../screens/WorkflowScreen';

const RootStack = createNativeStackNavigator<RootStackParamList>();
const MainStack = createNativeStackNavigator<MainStackParamList>();
const Tab       = createBottomTabNavigator<MainTabParamList>();

// ─────────────────────────────────────────────────────────
// TAB ICON — uses unicode symbols that render on all platforms
// without requiring a native font link.
// ─────────────────────────────────────────────────────────
interface TabIconProps {
  name: 'home' | 'upload' | 'history' | 'results' | 'profile';
  focused: boolean;
  color: string;
}

const ICON_MAP: Record<TabIconProps['name'], { active: string; inactive: string }> = {
  home:    { active: '⬛', inactive: '⬜' },   // replaced below with SVG paths
  upload:  { active: '✚', inactive: '✚' },
  history: { active: '◷', inactive: '◷' },
  results: { active: '◈', inactive: '◈' },
  profile: { active: '◉', inactive: '◉' },
};

function TabIcon({ name, focused, color }: TabIconProps) {
  if (name === 'upload') {
    // Special prominent upload button
    return (
      <View style={[
        styles.uploadIconOuter,
        focused && styles.uploadIconFocused,
      ]}>
        <LinearGradient
          colors={focused ? ['#3b82f6', '#06b6d4'] : ['#1e2d40', '#1e2d40']}
          style={styles.uploadIconInner}>
          <Text style={styles.uploadIconText}>↑</Text>
        </LinearGradient>
      </View>
    );
  }

  // Text-based icons — guaranteed to render without native linking
  const SYMBOLS: Record<string, string> = {
    home:    '⌂',
    history: '⧗',
    results: '⬡',
    profile: '⊙',
  };

  return (
    <View style={styles.tabIconWrap}>
      <Text style={[styles.tabIconText, { color, fontSize: name === 'home' ? 20 : 18 }]}>
        {SYMBOLS[name] || '•'}
      </Text>
    </View>
  );
}

// ─────────────────────────────────────────────────────────
// MAIN TABS
// ─────────────────────────────────────────────────────────
function MainTabs() {
  return (
    <Tab.Navigator
      screenOptions={{
        headerShown:         false,
        tabBarStyle:         styles.tabBar,
        tabBarActiveTintColor:   colors.accent,
        tabBarInactiveTintColor: colors.textMuted,
        tabBarLabelStyle:    styles.tabLabel,
        tabBarItemStyle:     styles.tabItem,
      }}>

      <Tab.Screen
        name="Dashboard"
        component={DashboardScreen}
        options={{
          tabBarLabel: 'Home',
          tabBarIcon: ({ focused, color }) => (
            <TabIcon name="home" focused={focused} color={color} />
          ),
        }}
      />

      <Tab.Screen
        name="Upload"
        component={UploadScreen}
        options={{
          tabBarLabel: '',
          tabBarIcon: ({ focused, color }) => (
            <TabIcon name="upload" focused={focused} color={color} />
          ),
          tabBarItemStyle: { ...styles.tabItem, marginTop: -6 },
        }}
      />

      <Tab.Screen
        name="History"
        component={HistoryScreen}
        options={{
          tabBarLabel: 'History',
          tabBarIcon: ({ focused, color }) => (
            <TabIcon name="history" focused={focused} color={color} />
          ),
        }}
      />

      <Tab.Screen
        name="Results"
        component={ResultsScreen}
        options={{
          tabBarLabel: 'Results',
          tabBarIcon: ({ focused, color }) => (
            <TabIcon name="results" focused={focused} color={color} />
          ),
        }}
      />

      <Tab.Screen
        name="Profile"
        component={ProfileScreen}
        options={{
          tabBarLabel: 'Profile',
          tabBarIcon: ({ focused, color }) => (
            <TabIcon name="profile" focused={focused} color={color} />
          ),
        }}
      />
    </Tab.Navigator>
  );
}

// ─────────────────────────────────────────────────────────
// MAIN STACK (tabs + workflow modal)
// ─────────────────────────────────────────────────────────
function MainStackNavigator() {
  return (
    <MainStack.Navigator screenOptions={{ headerShown: false }}>
      <MainStack.Screen name="Tabs"     component={MainTabs} />
      <MainStack.Screen
        name="Workflow"
        component={WorkflowScreen}
        options={{ presentation: 'modal', animation: 'slide_from_bottom' }}
      />
    </MainStack.Navigator>
  );
}

// ─────────────────────────────────────────────────────────
// ROOT STACK (auth + main)
// ─────────────────────────────────────────────────────────
export default function AppNavigator() {
  const { isAuthenticated, isLoading } = useAuth();

  if (isLoading) {
    return (
      <View style={styles.splash}>
        <LinearGradient
          colors={['#080c18', '#0f1623']}
          style={StyleSheet.absoluteFillObject}
        />
        <LinearGradient
          colors={['#3b82f6', '#06b6d4']}
          style={styles.splashLogo}>
          <Text style={styles.splashIcon}>⬡</Text>
        </LinearGradient>
        <Text style={styles.splashName}>DentAI</Text>
        <ActivityIndicator
          color={colors.accent}
          size="small"
          style={{ marginTop: 32 }}
        />
      </View>
    );
  }

  return (
    <NavigationContainer>
      <RootStack.Navigator
        screenOptions={{ headerShown: false, animation: 'fade' }}>
        {isAuthenticated ? (
          // Pass Main as a single screen — MainStackNavigator handles nested nav
          <RootStack.Screen name="Main" component={MainStackNavigator} />
        ) : (
          <>
            <RootStack.Screen name="Login"          component={LoginScreen} />
            <RootStack.Screen name="Signup"         component={SignupScreen} />
            <RootStack.Screen name="ForgotPassword" component={ForgotPasswordScreen} />
          </>
        )}
      </RootStack.Navigator>
    </NavigationContainer>
  );
}

// ─────────────────────────────────────────────────────────
const styles = StyleSheet.create({
  // ── Splash ─────────────────────────────────────────────
  splash: {
    flex: 1,
    alignItems: 'center',
    justifyContent: 'center',
    backgroundColor: colors.bgBase,
  },
  splashLogo: {
    width: 72,
    height: 72,
    borderRadius: 18,
    alignItems: 'center',
    justifyContent: 'center',
    ...shadows.glow,
  },
  splashIcon: { fontSize: 34, color: '#fff' },
  splashName: {
    fontSize: 28,
    fontWeight: '800',
    color: colors.accent,
    marginTop: 16,
    letterSpacing: -0.5,
  },

  // ── Tab bar ─────────────────────────────────────────────
  tabBar: {
    backgroundColor:  colors.bgCard,
    borderTopColor:   colors.border,
    borderTopWidth:   1,
    height:           Platform.select({ ios: 80, android: 64 }),
    paddingBottom:    Platform.select({ ios: 20, android: 6 }),
    paddingTop:       6,
    elevation:        12,
    shadowColor:      '#000',
    shadowOffset:     { width: 0, height: -4 },
    shadowOpacity:    0.4,
    shadowRadius:     16,
  },
  tabLabel: {
    fontSize: 10,
    fontWeight:    '600',
    letterSpacing:  0.3,
    marginTop:     -2,
  },
  tabItem: { paddingTop: 4 },

  // ── Tab icon ────────────────────────────────────────────
  tabIconWrap: {
    alignItems:      'center',
    justifyContent:  'center',
    width:            36,
    height:           28,
  },
  tabIconText: {
    textAlign:  'center',
    lineHeight:  22,
  },

  // ── Upload icon ─────────────────────────────────────────
  uploadIconOuter: {
    width:           56,
    height:          56,
    borderRadius:    28,
    marginBottom:     8,
    ...shadows.glow,
  },
  uploadIconFocused: {
    shadowOpacity: 0.7,
    shadowRadius:  16,
  },
  uploadIconInner: {
    flex:             1,
    borderRadius:     28,
    alignItems:       'center',
    justifyContent:   'center',
  },
  uploadIconText: {
    fontSize:    22,
    fontWeight:  '700',
    color:       '#fff',
    lineHeight:  26,
  },
});
