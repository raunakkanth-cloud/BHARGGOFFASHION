import React, { useState } from 'react';
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
  Image,
} from 'react-native';
import { useRouter } from 'expo-router';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../../constants/Colors';
import { LOGO_URL } from '../../constants/Logo';
import api from '../../utils/api';

export default function Register() {
  const router = useRouter();
  const [name, setName] = useState('');
  const [email, setEmail] = useState('');
  const [mobile, setMobile] = useState('');
  const [address, setAddress] = useState('');
  const [pincode, setPincode] = useState('');
  const [referralCode, setReferralCode] = useState('');
  const [subscribeNow, setSubscribeNow] = useState(false);
  const [loading, setLoading] = useState(false);

  const handleRegister = async () => {
    if (!name.trim()) { Alert.alert('Error', 'Please enter your name'); return; }
    if (!email.trim() || !email.includes('@')) { Alert.alert('Error', 'Please enter a valid email address'); return; }
    if (!mobile.trim() || mobile.trim().length < 10) { Alert.alert('Error', 'Please enter a valid 10-digit mobile number'); return; }
    if (!address.trim()) { Alert.alert('Error', 'Please enter your address'); return; }
    if (!pincode.trim() || pincode.trim().length < 6) { Alert.alert('Error', 'Please enter a valid 6-digit pin code'); return; }

    setLoading(true);
    try {
      const payload: any = {
        email: email.toLowerCase().trim(),
        name: name.trim(),
        mobile: mobile.trim(),
        address: address.trim(),
        pincode: pincode.trim(),
      };
      if (referralCode.trim()) {
        payload.sponsor_referral_id = referralCode.trim().toUpperCase();
      }

      const response = await api.post('/auth/register', payload);
      Alert.alert('Success', response.data.message);
      router.push({
        pathname: '/auth/verify-otp',
        params: { email: email.toLowerCase().trim(), mode: 'register', subscribe: subscribeNow ? 'yes' : 'no' },
      });
    } catch (error: any) {
      const message = error.response?.data?.detail || 'Registration failed. Please try again.';
      Alert.alert('Error', message);
    } finally {
      setLoading(false);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <KeyboardAvoidingView behavior={Platform.OS === 'ios' ? 'padding' : 'height'} style={styles.keyboardView}>
        <ScrollView contentContainerStyle={styles.scrollView} showsVerticalScrollIndicator={false}>
          <TouchableOpacity testID="register-back-btn" style={styles.backButton} onPress={() => router.back()}>
            <Ionicons name="arrow-back" size={24} color={Colors.text} />
          </TouchableOpacity>

          <View style={styles.header}>
            <Image source={{ uri: LOGO_URL }} style={styles.logo} />
          </View>

          <View style={styles.form}>
            <Text style={styles.title}>Create Account</Text>
            <Text style={styles.subtitle}>Fill in your details to get started</Text>

            <View style={styles.inputContainer}>
              <Ionicons name="person-outline" size={20} color={Colors.gray} style={styles.inputIcon} />
              <TextInput testID="register-name-input" style={styles.input} placeholder="Full Name" placeholderTextColor={Colors.gray} value={name} onChangeText={setName} autoCapitalize="words" />
            </View>

            <View style={styles.inputContainer}>
              <Ionicons name="mail-outline" size={20} color={Colors.gray} style={styles.inputIcon} />
              <TextInput testID="register-email-input" style={styles.input} placeholder="Email Address" placeholderTextColor={Colors.gray} value={email} onChangeText={setEmail} keyboardType="email-address" autoCapitalize="none" autoComplete="email" />
            </View>

            <View style={styles.inputContainer}>
              <Ionicons name="call-outline" size={20} color={Colors.gray} style={styles.inputIcon} />
              <Text style={styles.countryCode}>+91</Text>
              <TextInput testID="register-mobile-input" style={styles.input} placeholder="Mobile Number" placeholderTextColor={Colors.gray} value={mobile} onChangeText={setMobile} keyboardType="phone-pad" maxLength={10} />
            </View>

            <View style={[styles.inputContainer, styles.addressInput]}>
              <Ionicons name="location-outline" size={20} color={Colors.gray} style={styles.inputIcon} />
              <TextInput testID="register-address-input" style={[styles.input, { height: 80, textAlignVertical: 'top', paddingTop: 16 }]} placeholder="Full Address" placeholderTextColor={Colors.gray} value={address} onChangeText={setAddress} multiline numberOfLines={3} />
            </View>

            <View style={styles.inputContainer}>
              <Ionicons name="map-outline" size={20} color={Colors.gray} style={styles.inputIcon} />
              <TextInput testID="register-pincode-input" style={styles.input} placeholder="Pin Code" placeholderTextColor={Colors.gray} value={pincode} onChangeText={setPincode} keyboardType="number-pad" maxLength={6} />
            </View>

            <View style={styles.inputContainer}>
              <Ionicons name="gift-outline" size={20} color={Colors.gray} style={styles.inputIcon} />
              <TextInput testID="register-referral-input" style={styles.input} placeholder="Referral Code (Optional)" placeholderTextColor={Colors.gray} value={referralCode} onChangeText={setReferralCode} autoCapitalize="characters" />
            </View>

            {/* Subscription Option */}
            <TouchableOpacity
              testID="register-subscribe-toggle"
              style={[styles.subscribeCard, subscribeNow && styles.subscribeCardActive]}
              onPress={() => setSubscribeNow(!subscribeNow)}
            >
              <View style={styles.subscribeCardRow}>
                <View style={[styles.checkbox, subscribeNow && styles.checkboxActive]}>
                  {subscribeNow && <Ionicons name="checkmark" size={16} color={Colors.white} />}
                </View>
                <Ionicons name="diamond" size={24} color={Colors.primary} style={{ marginLeft: 12 }} />
                <View style={styles.subscribeCardText}>
                  <Text style={styles.subscribeCardTitle}>Premium Membership - ₹111</Text>
                  <Text style={styles.subscribeCardSubtitle}>20% off + Faster delivery + Referral earnings</Text>
                </View>
              </View>
            </TouchableOpacity>

            <TouchableOpacity testID="register-submit-btn" style={[styles.button, loading && styles.buttonDisabled]} onPress={handleRegister} disabled={loading}>
              {loading ? <ActivityIndicator color={Colors.white} /> : (
                <Text style={styles.buttonText}>{subscribeNow ? 'Continue & Pay ₹111' : 'Continue'}</Text>
              )}
            </TouchableOpacity>

            <View style={styles.footer}>
              <Text style={styles.footerText}>Already have an account? </Text>
              <TouchableOpacity testID="register-login-link" onPress={() => router.push('/auth/login')}>
                <Text style={styles.linkText}>Login</Text>
              </TouchableOpacity>
            </View>
          </View>
        </ScrollView>
      </KeyboardAvoidingView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.white },
  keyboardView: { flex: 1 },
  scrollView: { flexGrow: 1, padding: 24, paddingBottom: 40 },
  backButton: { width: 40, height: 40, borderRadius: 20, backgroundColor: Colors.lightGray, justifyContent: 'center', alignItems: 'center', marginBottom: 8 },
  header: { alignItems: 'center', marginBottom: 20 },
  logo: { width: 120, height: 120, resizeMode: 'contain' },
  form: { flex: 1 },
  title: { fontSize: 28, fontWeight: 'bold', color: Colors.text, marginBottom: 8 },
  subtitle: { fontSize: 15, color: Colors.textSecondary, marginBottom: 24 },
  inputContainer: { flexDirection: 'row', alignItems: 'center', borderWidth: 1, borderColor: Colors.border, borderRadius: 12, marginBottom: 14, paddingHorizontal: 16, backgroundColor: Colors.lightGray },
  addressInput: { alignItems: 'flex-start' },
  inputIcon: { marginRight: 12 },
  countryCode: { fontSize: 16, color: Colors.text, fontWeight: '600', marginRight: 8, paddingRight: 8, borderRightWidth: 1, borderRightColor: Colors.border },
  input: { flex: 1, height: 52, fontSize: 16, color: Colors.text },
  button: { backgroundColor: Colors.primary, height: 56, borderRadius: 12, justifyContent: 'center', alignItems: 'center', marginTop: 8 },
  buttonDisabled: { opacity: 0.6 },
  buttonText: { color: Colors.white, fontSize: 18, fontWeight: '600' },
  footer: { flexDirection: 'row', justifyContent: 'center', marginTop: 20 },
  footerText: { color: Colors.textSecondary, fontSize: 16 },
  linkText: { color: Colors.primary, fontSize: 16, fontWeight: '600' },
  subscribeCard: { borderWidth: 1.5, borderColor: Colors.border, borderRadius: 12, padding: 16, marginBottom: 14, backgroundColor: Colors.lightGray },
  subscribeCardActive: { borderColor: Colors.primary, backgroundColor: Colors.primary + '08' },
  subscribeCardRow: { flexDirection: 'row', alignItems: 'center' },
  checkbox: { width: 24, height: 24, borderRadius: 6, borderWidth: 2, borderColor: Colors.border, justifyContent: 'center', alignItems: 'center' },
  checkboxActive: { backgroundColor: Colors.primary, borderColor: Colors.primary },
  subscribeCardText: { flex: 1, marginLeft: 12 },
  subscribeCardTitle: { fontSize: 15, fontWeight: 'bold', color: Colors.text },
  subscribeCardSubtitle: { fontSize: 12, color: Colors.textSecondary, marginTop: 2 },
});
