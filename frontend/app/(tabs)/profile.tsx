import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Alert,
  Share,
  Image,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { Colors } from '../../constants/Colors';
import { LOGO_URL } from '../../constants/Logo';
import { useAuthStore } from '../../store/authStore';

export default function Profile() {
  const router = useRouter();
  const { user, isAuthenticated, logout } = useAuthStore();

  // Guest mode - show login prompt
  if (!isAuthenticated) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.guestContainer}>
          <Image source={{ uri: LOGO_URL }} style={styles.guestLogo} />
          <Text style={styles.guestTitle}>Join Bharggo Fashion</Text>
          <Text style={styles.guestSubtitle}>Login or register to access your profile, wallet, referral code, and exclusive benefits</Text>
          <TouchableOpacity testID="profile-guest-login-btn" style={styles.guestLoginBtn} onPress={() => router.push('/auth/login')}>
            <Text style={styles.guestLoginBtnText}>Login</Text>
          </TouchableOpacity>
          <TouchableOpacity testID="profile-guest-register-btn" style={styles.guestRegisterBtn} onPress={() => router.push('/auth/register')}>
            <Text style={styles.guestRegisterBtnText}>Create Account</Text>
          </TouchableOpacity>
        </View>
      </SafeAreaView>
    );
  }

  const handleShareReferral = async () => {
    try {
      await Share.share({ message: `Join Bharggo Fashion using my referral code: ${user?.referral_id}\n\nGet exclusive benefits and start earning!` });
    } catch (error) { console.error('Error sharing:', error); }
  };

  const handleLogout = () => {
    Alert.alert('Logout', 'Are you sure you want to logout?', [
      { text: 'Cancel', style: 'cancel' },
      { text: 'Logout', style: 'destructive', onPress: async () => { await logout(); router.replace('/(tabs)/home'); } },
    ]);
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Header */}
        <View style={styles.header}>
          <Image source={{ uri: LOGO_URL }} style={styles.headerLogo} />
          <View style={styles.avatar}>
            <Text style={styles.avatarText}>{user?.name?.charAt(0).toUpperCase()}</Text>
          </View>
          <Text style={styles.name}>{user?.name}</Text>
          <Text style={styles.email}>{user?.email}</Text>
        </View>

        {/* Subscription Status - optional */}
        {user?.subscription_status ? (
          <View style={styles.premiumBanner}>
            <Ionicons name="diamond" size={24} color={Colors.primary} />
            <View style={styles.premiumText}>
              <Text style={styles.premiumTitle}>Premium Member</Text>
              <Text style={styles.premiumSubtitle}>Enjoy exclusive benefits</Text>
            </View>
            <Ionicons name="checkmark-circle" size={24} color={Colors.success} />
          </View>
        ) : (
          <TouchableOpacity testID="profile-subscribe-btn" style={styles.subscribeBanner}>
            <View style={styles.subscribeContent}>
              <Ionicons name="diamond-outline" size={24} color={Colors.primary} />
              <View style={styles.subscribeText}>
                <Text style={styles.subscribeTitle}>Become Premium (Optional)</Text>
                <Text style={styles.subscribeSubtitle}>₹111 - Get 20% off + referral earnings</Text>
              </View>
              <Ionicons name="chevron-forward" size={24} color={Colors.primary} />
            </View>
          </TouchableOpacity>
        )}

        {/* Wallet Card */}
        <View style={styles.walletCard}>
          <View style={styles.walletHeader}>
            <View>
              <Text style={styles.walletLabel}>Wallet Balance</Text>
              <Text style={styles.walletAmount}>₹{user?.wallet_balance?.toFixed(2) || '0.00'}</Text>
            </View>
            <TouchableOpacity testID="profile-withdraw-btn" style={styles.walletButton}>
              <Text style={styles.walletButtonText}>Withdraw</Text>
            </TouchableOpacity>
          </View>
          <View style={styles.walletDivider} />
          <View style={styles.walletStats}>
            <View style={styles.walletStat}>
              <Text style={styles.walletStatValue}>₹{user?.total_commission_earned?.toFixed(2) || '0.00'}</Text>
              <Text style={styles.walletStatLabel}>Total Earned</Text>
            </View>
            <View style={styles.walletStatDivider} />
            <View style={styles.walletStat}>
              <Text style={styles.walletStatValue}>Level {user?.level || 0}</Text>
              <Text style={styles.walletStatLabel}>Your Level</Text>
            </View>
          </View>
        </View>

        {/* Referral Card */}
        <View style={styles.referralCard}>
          <View style={styles.referralHeader}>
            <Ionicons name="gift" size={24} color={Colors.primary} />
            <Text style={styles.referralTitle}>Your Referral Code</Text>
          </View>
          <View style={styles.referralCodeContainer}>
            <Text style={styles.referralCode}>{user?.referral_id}</Text>
            <TouchableOpacity testID="profile-share-referral-btn" onPress={handleShareReferral} style={styles.shareButton}>
              <Ionicons name="share-social" size={20} color={Colors.white} />
              <Text style={styles.shareButtonText}>Share</Text>
            </TouchableOpacity>
          </View>
          <Text style={styles.referralDescription}>Share your code and earn 1% commission on purchases up to 9 levels!</Text>
        </View>

        {/* Menu Options */}
        <View style={styles.menuSection}>
          <TouchableOpacity testID="profile-orders-btn" style={styles.menuItem} onPress={() => router.push('/orders')}>
            <View style={styles.menuItemLeft}><Ionicons name="receipt-outline" size={24} color={Colors.text} /><Text style={styles.menuItemText}>My Orders</Text></View>
            <Ionicons name="chevron-forward" size={20} color={Colors.gray} />
          </TouchableOpacity>
          <TouchableOpacity testID="profile-wishlist-btn" style={styles.menuItem}>
            <View style={styles.menuItemLeft}><Ionicons name="heart-outline" size={24} color={Colors.text} /><Text style={styles.menuItemText}>Wishlist</Text></View>
            <Ionicons name="chevron-forward" size={20} color={Colors.gray} />
          </TouchableOpacity>
          <TouchableOpacity testID="profile-referrals-btn" style={styles.menuItem}>
            <View style={styles.menuItemLeft}><Ionicons name="people-outline" size={24} color={Colors.text} /><Text style={styles.menuItemText}>My Referrals</Text></View>
            <Ionicons name="chevron-forward" size={20} color={Colors.gray} />
          </TouchableOpacity>
          <TouchableOpacity testID="profile-card-btn" style={styles.menuItem} onPress={() => router.push('/shopping-card')}>
            <View style={styles.menuItemLeft}><Ionicons name="card-outline" size={24} color={Colors.text} /><Text style={styles.menuItemText}>Digital Shopping Card</Text></View>
            <Ionicons name="chevron-forward" size={20} color={Colors.gray} />
          </TouchableOpacity>
        </View>

        {/* Legal Pages */}
        <View style={styles.menuSection}>
          <Text style={styles.menuSectionTitle}>Legal</Text>
          <TouchableOpacity style={styles.menuItem} onPress={() => router.push({ pathname: '/legal', params: { type: 'terms' } })}>
            <View style={styles.menuItemLeft}><Ionicons name="document-text-outline" size={24} color={Colors.text} /><Text style={styles.menuItemText}>Terms & Conditions</Text></View>
            <Ionicons name="chevron-forward" size={20} color={Colors.gray} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.menuItem} onPress={() => router.push({ pathname: '/legal', params: { type: 'privacy' } })}>
            <View style={styles.menuItemLeft}><Ionicons name="shield-checkmark-outline" size={24} color={Colors.text} /><Text style={styles.menuItemText}>Privacy Policy</Text></View>
            <Ionicons name="chevron-forward" size={20} color={Colors.gray} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.menuItem} onPress={() => router.push({ pathname: '/legal', params: { type: 'refund' } })}>
            <View style={styles.menuItemLeft}><Ionicons name="refresh-outline" size={24} color={Colors.text} /><Text style={styles.menuItemText}>Refund & Return Policy</Text></View>
            <Ionicons name="chevron-forward" size={20} color={Colors.gray} />
          </TouchableOpacity>
          <TouchableOpacity style={styles.menuItem} onPress={() => router.push({ pathname: '/legal', params: { type: 'shipping' } })}>
            <View style={styles.menuItemLeft}><Ionicons name="car-outline" size={24} color={Colors.text} /><Text style={styles.menuItemText}>Shipping Policy</Text></View>
            <Ionicons name="chevron-forward" size={20} color={Colors.gray} />
          </TouchableOpacity>
        </View>

        {/* Logout */}
        <View style={styles.menuSection}>
          <TouchableOpacity testID="profile-logout-btn" style={[styles.menuItem, styles.logoutItem]} onPress={handleLogout}>
            <View style={styles.menuItemLeft}><Ionicons name="log-out-outline" size={24} color={Colors.error} /><Text style={[styles.menuItemText, styles.logoutText]}>Logout</Text></View>
          </TouchableOpacity>
        </View>
        <View style={{ height: 40 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.lightGray },
  guestContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', paddingHorizontal: 40, backgroundColor: Colors.white },
  guestLogo: { width: 160, height: 160, resizeMode: 'contain', marginBottom: 24 },
  guestTitle: { fontSize: 24, fontWeight: 'bold', color: Colors.text, marginBottom: 12 },
  guestSubtitle: { fontSize: 15, color: Colors.textSecondary, textAlign: 'center', marginBottom: 32, lineHeight: 22 },
  guestLoginBtn: { backgroundColor: Colors.primary, width: '100%', height: 52, borderRadius: 12, justifyContent: 'center', alignItems: 'center', marginBottom: 12 },
  guestLoginBtnText: { color: Colors.white, fontSize: 18, fontWeight: '600' },
  guestRegisterBtn: { borderWidth: 2, borderColor: Colors.primary, width: '100%', height: 52, borderRadius: 12, justifyContent: 'center', alignItems: 'center' },
  guestRegisterBtnText: { color: Colors.primary, fontSize: 18, fontWeight: '600' },
  header: { backgroundColor: Colors.white, alignItems: 'center', paddingVertical: 24, paddingHorizontal: 20 },
  headerLogo: { width: 60, height: 60, resizeMode: 'contain', marginBottom: 12 },
  avatar: { width: 72, height: 72, borderRadius: 36, backgroundColor: Colors.primary, justifyContent: 'center', alignItems: 'center', marginBottom: 12 },
  avatarText: { fontSize: 28, fontWeight: 'bold', color: Colors.white },
  name: { fontSize: 22, fontWeight: 'bold', color: Colors.text, marginBottom: 4 },
  email: { fontSize: 14, color: Colors.textSecondary },
  premiumBanner: { flexDirection: 'row', alignItems: 'center', backgroundColor: Colors.white, margin: 16, padding: 16, borderRadius: 12, borderWidth: 2, borderColor: Colors.primary },
  premiumText: { flex: 1, marginLeft: 12 },
  premiumTitle: { fontSize: 16, fontWeight: 'bold', color: Colors.text },
  premiumSubtitle: { fontSize: 13, color: Colors.textSecondary, marginTop: 2 },
  subscribeBanner: { backgroundColor: Colors.white, margin: 16, borderRadius: 12, borderWidth: 1.5, borderColor: Colors.primary },
  subscribeContent: { flexDirection: 'row', alignItems: 'center', padding: 16 },
  subscribeText: { flex: 1, marginLeft: 12 },
  subscribeTitle: { fontSize: 15, fontWeight: 'bold', color: Colors.text },
  subscribeSubtitle: { fontSize: 13, color: Colors.textSecondary, marginTop: 2 },
  walletCard: { backgroundColor: Colors.white, margin: 16, marginTop: 0, padding: 20, borderRadius: 12 },
  walletHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center' },
  walletLabel: { fontSize: 14, color: Colors.textSecondary, marginBottom: 4 },
  walletAmount: { fontSize: 32, fontWeight: 'bold', color: Colors.primary },
  walletButton: { backgroundColor: Colors.primary, paddingHorizontal: 20, paddingVertical: 10, borderRadius: 20 },
  walletButtonText: { color: Colors.white, fontSize: 14, fontWeight: '600' },
  walletDivider: { height: 1, backgroundColor: Colors.border, marginVertical: 16 },
  walletStats: { flexDirection: 'row' },
  walletStat: { flex: 1, alignItems: 'center' },
  walletStatValue: { fontSize: 18, fontWeight: 'bold', color: Colors.text, marginBottom: 4 },
  walletStatLabel: { fontSize: 13, color: Colors.textSecondary },
  walletStatDivider: { width: 1, backgroundColor: Colors.border, marginHorizontal: 16 },
  referralCard: { backgroundColor: Colors.white, margin: 16, marginTop: 0, padding: 20, borderRadius: 12 },
  referralHeader: { flexDirection: 'row', alignItems: 'center', marginBottom: 16 },
  referralTitle: { fontSize: 16, fontWeight: 'bold', color: Colors.text, marginLeft: 12 },
  referralCodeContainer: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', marginBottom: 12 },
  referralCode: { fontSize: 22, fontWeight: 'bold', color: Colors.primary, letterSpacing: 2 },
  shareButton: { flexDirection: 'row', backgroundColor: Colors.primary, paddingHorizontal: 16, paddingVertical: 10, borderRadius: 20, alignItems: 'center' },
  shareButtonText: { color: Colors.white, fontSize: 14, fontWeight: '600', marginLeft: 6 },
  referralDescription: { fontSize: 13, color: Colors.textSecondary, lineHeight: 18 },
  menuSection: { backgroundColor: Colors.white, marginHorizontal: 16, marginBottom: 16, borderRadius: 12, overflow: 'hidden' },
  menuSectionTitle: { fontSize: 14, fontWeight: '600', color: Colors.textSecondary, paddingHorizontal: 20, paddingTop: 16, paddingBottom: 8 },
  menuItem: { flexDirection: 'row', alignItems: 'center', justifyContent: 'space-between', paddingVertical: 16, paddingHorizontal: 20, borderBottomWidth: 1, borderBottomColor: Colors.border },
  menuItemLeft: { flexDirection: 'row', alignItems: 'center' },
  menuItemText: { fontSize: 16, color: Colors.text, marginLeft: 16, fontWeight: '500' },
  logoutItem: { borderBottomWidth: 0 },
  logoutText: { color: Colors.error },
});
