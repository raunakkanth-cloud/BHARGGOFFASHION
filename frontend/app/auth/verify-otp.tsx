import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  TextInput,
  TouchableOpacity,
  StyleSheet,
  KeyboardAvoidingView,
  Platform,
  ScrollView,
  Alert,
  ActivityIndicator,
} from 'react-native';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import AsyncStorage from '@react-native-async-storage/async-storage';
import { Colors } from '../../constants/Colors';
import api from '../../utils/api';
import { useAuthStore } from '../../store/authStore';

export default function VerifyOTP() {
  const router = useRouter();
  const params = useLocalSearchParams();
  const { email, mode, subscribe } = params;
  const { setUser, setToken } = useAuthStore();
  
  const [otp, setOtp] = useState('');
  const [loading, setLoading] = useState(false);
  const [resending, setResending] = useState(false);
  const [timer, setTimer] = useState(60);

  useEffect(() => {
    const interval = setInterval(() => {
      setTimer((prev) => (prev > 0 ? prev - 1 : 0));
    }, 1000);
    return () => clearInterval(interval);
  }, []);

  const handleVerifyOTP = async () => {
    if (!otp.trim() || otp.length !== 6) {
      Alert.alert('Error', 'Please enter a valid 6-digit OTP');
      return;
    }

    setLoading(true);
    try {
      const response = await api.post('/auth/verify-otp', {
        email: email,
        otp: otp.trim(),
      });

      const { token, user } = response.data;
      
      // Save auth data
      await setToken(token);
      await AsyncStorage.setItem('user_data', JSON.stringify(user));
      setUser(user);

      // Auto-subscribe if selected during registration
      const userId = user._id || user.id;
      if (mode === 'register' && subscribe === 'yes' && userId) {
        try {
          await api.post(`/subscription/${userId}/subscribe`);
          // Update user data with subscription
          const updatedUser = { ...user, subscription_status: true };
          await AsyncStorage.setItem('user_data', JSON.stringify(updatedUser));
          setUser(updatedUser);
          Alert.alert(
            'Welcome to Bharggo Fashion!',
            'Registration successful! You are now a Premium Member with 20% off on all purchases.',
            [{ text: 'Start Shopping', onPress: () => router.replace('/(tabs)/home') }]
          );
        } catch (subErr) {
          Alert.alert(
            'Registration Successful',
            'Account created! Subscription payment will be processed later.',
            [{ text: 'OK', onPress: () => router.replace('/(tabs)/home') }]
          );
        }
      } else {
        Alert.alert(
          'Success',
          mode === 'register' ? 'Registration successful!' : 'Login successful!',
          [{ text: 'OK', onPress: () => router.replace('/(tabs)/home') }]
        );
      }
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Invalid OTP. Please try again.';
      Alert.alert('Error', message);
    } finally {
      setLoading(false);
    }
  };

  const handleResendOTP = async () => {
    setResending(true);
    try {
      await api.post('/auth/resend-otp', { email });
      Alert.alert('Success', 'OTP resent to your email');
      setTimer(60);
      setOtp('');
    } catch (error: any) {
      Alert.alert('Error', 'Failed to resend OTP. Please try again.');
    } finally {
      setResending(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView
        behavior={Platform.OS === 'ios' ? 'padding' : 'height'}
        style={styles.keyboardView}
      >
        <ScrollView contentContainerStyle={styles.scrollView}>
          <TouchableOpacity style={styles.backButton} onPress={() => router.back()}>
            <Ionicons name="arrow-back" size={24} color={Colors.text} />
          </TouchableOpacity>

          <View style={styles.iconContainer}>
            <View style={styles.iconCircle}>
              <Ionicons name="mail" size={48} color={Colors.primary} />
            </View>
          </View>

          <View style={styles.content}>
            <Text style={styles.title}>Verify Your Email</Text>
            <Text style={styles.subtitle}>
              We've sent a 6-digit code to{' \n'}
              <Text style={styles.email}>{email}</Text>
            </Text>

            <View style={styles.otpContainer}>
              <TextInput
                style={styles.otpInput}
                placeholder="Enter OTP"
                placeholderTextColor={Colors.gray}
                value={otp}
                onChangeText={setOtp}
                keyboardType="number-pad"
                maxLength={6}
                textAlign="center"
              />
            </View>

            <TouchableOpacity
              style={[styles.button, loading && styles.buttonDisabled]}
              onPress={handleVerifyOTP}
              disabled={loading}
            >
              {loading ? (
                <ActivityIndicator color={Colors.white} />
              ) : (
                <Text style={styles.buttonText}>Verify OTP</Text>
              )}
            </TouchableOpacity>

            <View style={styles.resendContainer}>
              {timer > 0 ? (
                <Text style={styles.timerText}>Resend OTP in {timer}s</Text>
              ) : (
                <TouchableOpacity onPress={handleResendOTP} disabled={resending}>
                  <Text style={styles.resendText}>
                    {resending ? 'Sending...' : 'Resend OTP'}
                  </Text>
                </TouchableOpacity>
              )}
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.white,
  },
  keyboardView: {
    flex: 1,
  },
  scrollView: {
    flexGrow: 1,
    padding: 24,
  },
  backButton: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: Colors.lightGray,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 24,
  },
  iconContainer: {
    alignItems: 'center',
    marginVertical: 32,
  },
  iconCircle: {
    width: 120,
    height: 120,
    borderRadius: 60,
    backgroundColor: Colors.lightGray,
    justifyContent: 'center',
    alignItems: 'center',
  },
  content: {
    flex: 1,
  },
  title: {
    fontSize: 28,
    fontWeight: 'bold',
    color: Colors.text,
    textAlign: 'center',
    marginBottom: 12,
  },
  subtitle: {
    fontSize: 16,
    color: Colors.textSecondary,
    textAlign: 'center',
    marginBottom: 32,
  },
  email: {
    color: Colors.primary,
    fontWeight: '600',
  },
  otpContainer: {
    marginBottom: 24,
  },
  otpInput: {
    height: 64,
    borderWidth: 2,
    borderColor: Colors.border,
    borderRadius: 12,
    fontSize: 24,
    fontWeight: 'bold',
    color: Colors.text,
    letterSpacing: 8,
  },
  button: {
    backgroundColor: Colors.primary,
    height: 56,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  buttonDisabled: {
    opacity: 0.6,
  },
  buttonText: {
    color: Colors.white,
    fontSize: 18,
    fontWeight: '600',
  },
  resendContainer: {
    alignItems: 'center',
    marginTop: 24,
  },
  timerText: {
    color: Colors.textSecondary,
    fontSize: 16,
  },
  resendText: {
    color: Colors.primary,
    fontSize: 16,
    fontWeight: '600',
  },
});
