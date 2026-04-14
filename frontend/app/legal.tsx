import React from 'react';
import { View, Text, StyleSheet, ScrollView, TouchableOpacity } from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Colors } from '../constants/Colors';

const LEGAL_CONTENT: Record<string, { title: string; content: string[] }> = {
  terms: {
    title: 'Terms & Conditions',
    content: [
      'Welcome to Bharggo FFashion India Pvt. Ltd. By using our application, you agree to the following terms:',
      '1. ACCEPTANCE OF TERMS\nBy accessing and using the Bharggo Fashion app, you accept and agree to be bound by the terms and provisions of this agreement.',
      '2. USER REGISTRATION\nYou must provide accurate and complete information during registration. You are responsible for maintaining the confidentiality of your account credentials.',
      '3. SUBSCRIPTION\nThe premium subscription costs ₹111 (one-time payment). Benefits include 20% discount on purchases, faster delivery, and access to referral earnings.',
      '4. REFERRAL PROGRAM\nUsers earn 1% commission on purchases made by their referrals, up to 9 levels deep. Commissions are valid for 31 days from the date of credit. Unclaimed commissions after 31 days will be transferred to the admin accounts.',
      '5. WALLET\nWallet balance can be used for purchases within the app. Withdrawals are allowed twice per month, subject to admin approval.',
      '6. PAYOUT\nPayment methods include UPI and bank transfer. All payouts require admin approval and are processed within 5-7 business days.',
      '7. PRODUCT INFORMATION\nWe strive to provide accurate product descriptions and images. However, slight variations may occur in actual products.',
      '8. MODIFICATIONS\nBharggo FFashion India Pvt. Ltd. reserves the right to modify these terms at any time without prior notice.',
    ],
  },
  privacy: {
    title: 'Privacy Policy',
    content: [
      'Bharggo FFashion India Pvt. Ltd. is committed to protecting your privacy.',
      '1. INFORMATION WE COLLECT\nWe collect personal information including name, email, mobile number, address, pin code, and transaction data to provide our services.',
      '2. HOW WE USE YOUR DATA\n- To process orders and deliver products\n- To manage your wallet and commissions\n- To send OTP for authentication\n- To improve our services and user experience\n- To communicate important updates',
      '3. DATA SECURITY\nWe implement industry-standard security measures including JWT authentication, encrypted data transmission, and secure payment processing.',
      '4. THIRD PARTY SHARING\nWe do not sell your personal information. We may share data with payment processors and delivery partners solely for order fulfillment.',
      '5. DATA RETENTION\nWe retain your data for as long as your account is active. You may request data deletion by contacting our support team.',
      '6. COOKIES & TRACKING\nOur app may use local storage for session management and improving user experience.',
    ],
  },
  refund: {
    title: 'Refund & Return Policy',
    content: [
      'At Bharggo Fashion, we want you to be completely satisfied with your purchase.',
      '1. RETURN WINDOW\nYou may request a return within 7 days of delivery for most products.',
      '2. RETURN CONDITIONS\n- Products must be unused and in original packaging\n- Tags must be intact\n- Items should not be damaged by the customer\n- Certain items like innerwear and personalized products are non-returnable',
      '3. REFUND PROCESS\n- Once we receive and inspect the returned item, your refund will be processed within 5-7 business days\n- Refunds will be credited to your original payment method or wallet',
      '4. EXCHANGE\nExchanges are subject to product availability. If the desired product is unavailable, a full refund will be issued.',
      '5. SUBSCRIPTION REFUND\nThe ₹111 subscription fee is non-refundable once activated.',
      '6. COMMISSION REFUND\nIf an order associated with referral commissions is returned, the corresponding commissions will be reversed.',
    ],
  },
  shipping: {
    title: 'Shipping Policy',
    content: [
      'Bharggo Fashion provides reliable shipping across India.',
      '1. DELIVERY TIME\n- Standard delivery: 5-7 business days\n- Premium members: 3-5 business days (priority shipping)',
      '2. SHIPPING CHARGES\n- Free shipping on orders above ₹499\n- ₹49 flat rate for orders below ₹499\n- Premium members enjoy free shipping on all orders',
      '3. TRACKING\nOrder tracking is available through the app. You will receive updates on your order status.',
      '4. DELIVERY AREAS\nWe currently deliver across India. Remote areas may require additional delivery time.',
      '5. FAILED DELIVERY\nIf delivery fails after 3 attempts, the order will be returned to our warehouse and a refund will be initiated.',
      '6. DAMAGED PRODUCTS\nIf you receive a damaged product, please report it within 24 hours through the app for immediate resolution.',
    ],
  },
};

export default function LegalPage() {
  const router = useRouter();
  const { type } = useLocalSearchParams();
  const pageType = (type as string) || 'terms';
  const page = LEGAL_CONTENT[pageType] || LEGAL_CONTENT.terms;

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity testID="legal-back-btn" onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>{page.title}</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
        {page.content.map((section, index) => (
          <Text key={index} style={[styles.text, index === 0 && styles.intro]}>
            {section}
          </Text>
        ))}

        <View style={styles.footer}>
          <Text style={styles.footerText}>Bharggo FFashion India Pvt. Ltd.</Text>
          <Text style={styles.footerDate}>Last updated: January 2026</Text>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.white,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 16,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  backBtn: {
    width: 40,
    height: 40,
    borderRadius: 20,
    backgroundColor: Colors.lightGray,
    justifyContent: 'center',
    alignItems: 'center',
  },
  headerTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: Colors.text,
  },
  content: {
    padding: 20,
    paddingBottom: 40,
  },
  intro: {
    fontSize: 16,
    fontWeight: '500',
    marginBottom: 20,
  },
  text: {
    fontSize: 14,
    color: Colors.text,
    lineHeight: 22,
    marginBottom: 16,
  },
  footer: {
    marginTop: 32,
    padding: 20,
    backgroundColor: Colors.lightGray,
    borderRadius: 12,
    alignItems: 'center',
  },
  footerText: {
    fontSize: 14,
    fontWeight: '600',
    color: Colors.text,
  },
  footerDate: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 4,
  },
});
