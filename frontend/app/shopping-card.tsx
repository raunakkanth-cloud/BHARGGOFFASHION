import React from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Share,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { Colors } from '../constants/Colors';
import { useAuthStore } from '../store/authStore';

export default function ShoppingCard() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);

  const handleShare = async () => {
    try {
      await Share.share({
        message: `Bharggo Fashion Shopping Card\n\nName: ${user?.name}\nReferral ID: ${user?.referral_id}\nMember since: ${new Date(user?.created_at || '').toLocaleDateString()}\n\nDownload Bharggo Fashion App and use my referral code to get exclusive benefits!`,
      });
    } catch (error) {
      console.error('Error sharing:', error);
    }
  };

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity testID="card-back-btn" onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>Digital Shopping Card</Text>
        <View style={{ width: 40 }} />
      </View>

      <ScrollView contentContainerStyle={styles.content}>
        {/* Front of Card */}
        <View style={styles.card}>
          <View style={styles.cardTopStrip} />
          <View style={styles.cardContent}>
            <View style={styles.cardHeader}>
              <View style={styles.cardLogo}>
                <Text style={styles.cardLogoText}>B</Text>
              </View>
              <View>
                <Text style={styles.cardBrand}>BHARGGO</Text>
                <Text style={styles.cardBrandSub}>FASHION INDIA</Text>
              </View>
            </View>

            {/* Chip */}
            <View style={styles.chipContainer}>
              <View style={styles.chip}>
                <View style={styles.chipLines}>
                  <View style={styles.chipLine} />
                  <View style={styles.chipLine} />
                  <View style={styles.chipLine} />
                </View>
              </View>
            </View>

            {/* Referral ID */}
            <View style={styles.cardIdContainer}>
              <Text style={styles.cardIdLabel}>REFERRAL ID</Text>
              <Text style={styles.cardId}>{user?.referral_id || 'XXXXXXXXXXXX'}</Text>
            </View>

            {/* Name */}
            <View style={styles.cardNameContainer}>
              <View>
                <Text style={styles.cardNameLabel}>CARD HOLDER</Text>
                <Text style={styles.cardName}>{user?.name?.toUpperCase() || 'MEMBER NAME'}</Text>
              </View>
              <View style={styles.memberBadge}>
                <Text style={styles.memberBadgeText}>
                  {user?.subscription_status ? 'PREMIUM' : 'MEMBER'}
                </Text>
              </View>
            </View>
          </View>
          <View style={styles.cardBottomStrip} />
        </View>

        {/* Card Details */}
        <View style={styles.detailsCard}>
          <Text style={styles.detailsTitle}>Card Details</Text>
          
          <View style={styles.detailRow}>
            <Ionicons name="person-outline" size={20} color={Colors.gray} />
            <View style={styles.detailInfo}>
              <Text style={styles.detailLabel}>Card Holder</Text>
              <Text style={styles.detailValue}>{user?.name}</Text>
            </View>
          </View>

          <View style={styles.detailRow}>
            <Ionicons name="mail-outline" size={20} color={Colors.gray} />
            <View style={styles.detailInfo}>
              <Text style={styles.detailLabel}>Email</Text>
              <Text style={styles.detailValue}>{user?.email}</Text>
            </View>
          </View>

          <View style={styles.detailRow}>
            <Ionicons name="barcode-outline" size={20} color={Colors.gray} />
            <View style={styles.detailInfo}>
              <Text style={styles.detailLabel}>Referral ID</Text>
              <Text style={styles.detailValue}>{user?.referral_id}</Text>
            </View>
          </View>

          <View style={styles.detailRow}>
            <Ionicons name="diamond-outline" size={20} color={Colors.gray} />
            <View style={styles.detailInfo}>
              <Text style={styles.detailLabel}>Status</Text>
              <Text style={[styles.detailValue, { color: user?.subscription_status ? Colors.success : Colors.primary }]}>
                {user?.subscription_status ? 'Premium Member' : 'Standard Member'}
              </Text>
            </View>
          </View>
        </View>

        {/* Action Buttons */}
        <View style={styles.actions}>
          <TouchableOpacity testID="card-share-btn" style={styles.actionBtn} onPress={handleShare}>
            <Ionicons name="share-social" size={24} color={Colors.white} />
            <Text style={styles.actionBtnText}>Share Card</Text>
          </TouchableOpacity>
        </View>
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.lightGray,
  },
  header: {
    flexDirection: 'row',
    alignItems: 'center',
    justifyContent: 'space-between',
    paddingHorizontal: 20,
    paddingVertical: 16,
    backgroundColor: Colors.white,
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
  card: {
    borderRadius: 16,
    overflow: 'hidden',
    backgroundColor: '#1C1C2E',
    shadowColor: '#000',
    shadowOffset: { width: 0, height: 8 },
    shadowOpacity: 0.3,
    shadowRadius: 16,
    elevation: 12,
    marginBottom: 24,
  },
  cardTopStrip: {
    height: 4,
    backgroundColor: Colors.primary,
  },
  cardContent: {
    padding: 24,
  },
  cardHeader: {
    flexDirection: 'row',
    alignItems: 'center',
    marginBottom: 24,
  },
  cardLogo: {
    width: 44,
    height: 44,
    borderRadius: 22,
    backgroundColor: Colors.primary,
    justifyContent: 'center',
    alignItems: 'center',
    marginRight: 12,
  },
  cardLogoText: {
    fontSize: 24,
    fontWeight: 'bold',
    color: Colors.white,
  },
  cardBrand: {
    fontSize: 20,
    fontWeight: 'bold',
    color: Colors.white,
    letterSpacing: 4,
  },
  cardBrandSub: {
    fontSize: 10,
    color: '#888',
    letterSpacing: 3,
  },
  chipContainer: {
    marginBottom: 20,
  },
  chip: {
    width: 48,
    height: 36,
    borderRadius: 6,
    backgroundColor: '#D4AF37',
    justifyContent: 'center',
    paddingHorizontal: 4,
  },
  chipLines: {
    gap: 3,
  },
  chipLine: {
    height: 2,
    backgroundColor: '#B8962E',
    borderRadius: 1,
  },
  cardIdContainer: {
    marginBottom: 20,
  },
  cardIdLabel: {
    fontSize: 10,
    color: '#888',
    letterSpacing: 2,
    marginBottom: 4,
  },
  cardId: {
    fontSize: 22,
    fontWeight: 'bold',
    color: Colors.white,
    letterSpacing: 3,
  },
  cardNameContainer: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-end',
  },
  cardNameLabel: {
    fontSize: 10,
    color: '#888',
    letterSpacing: 2,
    marginBottom: 4,
  },
  cardName: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.white,
    letterSpacing: 1,
  },
  memberBadge: {
    backgroundColor: Colors.primary,
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  memberBadgeText: {
    fontSize: 11,
    fontWeight: 'bold',
    color: Colors.white,
    letterSpacing: 1,
  },
  cardBottomStrip: {
    height: 4,
    backgroundColor: Colors.secondary,
  },
  detailsCard: {
    backgroundColor: Colors.white,
    borderRadius: 12,
    padding: 20,
    marginBottom: 24,
  },
  detailsTitle: {
    fontSize: 18,
    fontWeight: 'bold',
    color: Colors.text,
    marginBottom: 16,
  },
  detailRow: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 12,
    borderBottomWidth: 1,
    borderBottomColor: Colors.border,
  },
  detailInfo: {
    marginLeft: 16,
    flex: 1,
  },
  detailLabel: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginBottom: 2,
  },
  detailValue: {
    fontSize: 16,
    fontWeight: '600',
    color: Colors.text,
  },
  actions: {
    gap: 12,
  },
  actionBtn: {
    flexDirection: 'row',
    backgroundColor: Colors.primary,
    height: 56,
    borderRadius: 12,
    justifyContent: 'center',
    alignItems: 'center',
  },
  actionBtnText: {
    color: Colors.white,
    fontSize: 18,
    fontWeight: '600',
    marginLeft: 12,
  },
});
