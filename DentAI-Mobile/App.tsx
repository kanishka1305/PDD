/**
 * DentAI Mobile
 * React Native App — same dark medical theme as the web UI
 * Connects to FastAPI backend at BASE_URL (default: http://10.0.2.2:8000)
 */
import React from 'react';
import { StatusBar } from 'react-native';
import { GestureHandlerRootView } from 'react-native-gesture-handler';
import Toast from 'react-native-toast-message';
import { AuthProvider } from './src/context/AuthContext';
import AppNavigator from './src/navigation/AppNavigator';
import { colors } from './src/utils/theme';

export default function App() {
  return (
    <GestureHandlerRootView style={{ flex: 1 }}>
      <StatusBar barStyle="light-content" backgroundColor={colors.bgBase} />
      <AuthProvider>
        <AppNavigator />
      </AuthProvider>
      <Toast />
    </GestureHandlerRootView>
  );
}
