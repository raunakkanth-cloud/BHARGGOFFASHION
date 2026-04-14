import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  RefreshControl,
  Dimensions,
  Image,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { useAuthStore } from '../../store/authStore';
import { Colors } from '../../constants/Colors';
import api from '../../utils/api';

const { width } = Dimensions.get('window');

const CATEGORY_ICONS: Record<string, string> = {
  Men: 'man',
  Women: 'woman',
  Kids: 'happy',
};

export default function Home() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);
  const [refreshing, setRefreshing] = useState(false);
  const [categories, setCategories] = useState<string[]>([]);
  const [products, setProducts] = useState<any[]>([]);

  useEffect(() => {
    fetchData();
  }, []);

  const fetchData = async () => {
    try {
      const [categoriesRes, productsRes] = await Promise.all([
        api.get('/categories'),
        api.get('/products?limit=10'),
      ]);
      setCategories(categoriesRes.data.categories || []);
      setProducts(productsRes.data.products || []);
    } catch (error) {
      console.error('Error fetching data:', error);
    }
  };

  const onRefresh = async () => {
    setRefreshing(true);
    await fetchData();
    setRefreshing(false);
  };

  return (
    <SafeAreaView style={styles.container}>
      <ScrollView
        showsVerticalScrollIndicator={false}
        refreshControl={
          <RefreshControl refreshing={refreshing} onRefresh={onRefresh} tintColor={Colors.primary} />
        }
      >
        {/* Header */}
        <View style={styles.header}>
          <View>
            <Text style={styles.greeting}>Hello, {user?.name || 'Guest'}!</Text>
            <Text style={styles.subGreeting}>Welcome to Bharggo Fashion</Text>
          </View>
          <TouchableOpacity testID="home-notification-btn" style={styles.notificationButton}>
            <Ionicons name="notifications-outline" size={24} color={Colors.text} />
          </TouchableOpacity>
        </View>

        {/* Banner */}
        <View style={styles.banner}>
          <View style={styles.bannerContent}>
            <Text style={styles.bannerTitle}>Premium{'\n'}Fashion</Text>
            <Text style={styles.bannerSubtitle}>Exclusive Collection 2026</Text>
            <TouchableOpacity testID="home-shop-now-btn" style={styles.bannerButton}>
              <Text style={styles.bannerButtonText}>Shop Now</Text>
            </TouchableOpacity>
          </View>
        </View>

        {/* Subscription Banner */}
        {!user?.subscription_status && (
          <TouchableOpacity testID="home-subscribe-btn" style={styles.subscriptionBanner}>
            <View style={styles.subscriptionContent}>
              <Ionicons name="diamond" size={28} color={Colors.primary} />
              <View style={styles.subscriptionText}>
                <Text style={styles.subscriptionTitle}>Become a Premium Member</Text>
                <Text style={styles.subscriptionSubtitle}>
                  Get 20% off + Referral earnings for just ₹111
                </Text>
              </View>
              <Ionicons name="chevron-forward" size={24} color={Colors.primary} />
            </View>
          </TouchableOpacity>
        )}

        {/* Categories */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Categories</Text>
          </View>
          <ScrollView horizontal showsHorizontalScrollIndicator={false} contentContainerStyle={styles.categoriesScroll}>
            {categories.length > 0 ? (
              categories.map((category, index) => (
                <TouchableOpacity key={index} style={styles.categoryCard}>
                  <View style={styles.categoryIcon}>
                    <Ionicons
                      name={(CATEGORY_ICONS[category] || 'shirt') as any}
                      size={32}
                      color={Colors.primary}
                    />
                  </View>
                  <Text style={styles.categoryText}>{category}</Text>
                </TouchableOpacity>
              ))
            ) : (
              <View style={styles.emptyCategories}>
                <Text style={styles.emptyText}>Loading categories...</Text>
              </View>
            )}
          </ScrollView>
        </View>

        {/* Trending Products */}
        <View style={styles.section}>
          <View style={styles.sectionHeader}>
            <Text style={styles.sectionTitle}>Trending Now</Text>
            <TouchableOpacity>
              <Text style={styles.seeAll}>See All</Text>
            </TouchableOpacity>
          </View>
          <View style={styles.productsGrid}>
            {products.length > 0 ? (
              products.slice(0, 6).map((product: any) => (
                <TouchableOpacity key={product._id} style={styles.productCard}>
                  {product.image_url ? (
                    <Image
                      source={{ uri: product.image_url }}
                      style={styles.productImage}
                    />
                  ) : (
                    <View style={styles.productImagePlaceholder}>
                      <Ionicons name="image-outline" size={48} color={Colors.gray} />
                    </View>
                  )}
                  <View style={styles.productInfo}>
                    <Text style={styles.productName} numberOfLines={2}>
                      {product.name}
                    </Text>
                    <View style={styles.productFooter}>
                      <View>
                        <Text style={styles.productPrice}>₹{product.price - (product.price * product.discount / 100)}</Text>
                        {product.discount > 0 && (
                          <View style={styles.discountRow}>
                            <Text style={styles.originalPrice}>₹{product.price}</Text>
                            <Text style={styles.productDiscount}>{product.discount}% OFF</Text>
                          </View>
                        )}
                      </View>
                      {product.rating > 0 && (
                        <View style={styles.ratingBadge}>
                          <Ionicons name="star" size={12} color={Colors.white} />
                          <Text style={styles.ratingText}>{product.rating}</Text>
                        </View>
                      )}
                    </View>
                  </View>
                </TouchableOpacity>
              ))
            ) : (
              <View style={styles.emptyProducts}>
                <Text style={styles.emptyText}>No products available yet</Text>
                <Text style={styles.emptySubtext}>Check back soon for amazing deals!</Text>
              </View>
            )}
          </View>
        </View>

        <View style={{ height: 20 }} />
      </ScrollView>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.white },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: 20, paddingVertical: 16 },
  greeting: { fontSize: 24, fontWeight: 'bold', color: Colors.text },
  subGreeting: { fontSize: 14, color: Colors.textSecondary, marginTop: 4 },
  notificationButton: { width: 44, height: 44, borderRadius: 22, backgroundColor: Colors.lightGray, justifyContent: 'center', alignItems: 'center' },
  banner: { marginHorizontal: 20, marginVertical: 16, height: 180, borderRadius: 16, overflow: 'hidden', backgroundColor: Colors.primary },
  bannerContent: { flex: 1, padding: 24, justifyContent: 'center' },
  bannerTitle: { fontSize: 28, fontWeight: 'bold', color: Colors.white, marginBottom: 4 },
  bannerSubtitle: { fontSize: 14, color: Colors.white, marginBottom: 16, opacity: 0.9 },
  bannerButton: { backgroundColor: Colors.white, paddingHorizontal: 24, paddingVertical: 12, borderRadius: 24, alignSelf: 'flex-start' },
  bannerButtonText: { color: Colors.primary, fontSize: 16, fontWeight: '600' },
  subscriptionBanner: { marginHorizontal: 20, marginBottom: 16, borderRadius: 12, backgroundColor: Colors.lightGray, borderWidth: 2, borderColor: Colors.primary },
  subscriptionContent: { flexDirection: 'row', alignItems: 'center', padding: 16 },
  subscriptionText: { flex: 1, marginLeft: 16 },
  subscriptionTitle: { fontSize: 16, fontWeight: 'bold', color: Colors.text, marginBottom: 4 },
  subscriptionSubtitle: { fontSize: 14, color: Colors.textSecondary },
  section: { marginTop: 8 },
  sectionHeader: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: 20, marginBottom: 16 },
  sectionTitle: { fontSize: 20, fontWeight: 'bold', color: Colors.text },
  seeAll: { fontSize: 14, color: Colors.primary, fontWeight: '600' },
  categoriesScroll: { paddingLeft: 20, paddingRight: 12 },
  categoryCard: { alignItems: 'center', marginRight: 16, width: 80 },
  categoryIcon: { width: 64, height: 64, borderRadius: 32, backgroundColor: Colors.lightGray, justifyContent: 'center', alignItems: 'center', marginBottom: 8 },
  categoryText: { fontSize: 13, color: Colors.text, textAlign: 'center', fontWeight: '500' },
  productsGrid: { flexDirection: 'row', flexWrap: 'wrap', paddingHorizontal: 12 },
  productCard: { width: (width - 48) / 2, margin: 8, backgroundColor: Colors.white, borderRadius: 12, overflow: 'hidden', borderWidth: 1, borderColor: Colors.border },
  productImage: { width: '100%', height: 160 },
  productImagePlaceholder: { width: '100%', height: 160, backgroundColor: Colors.lightGray, justifyContent: 'center', alignItems: 'center' },
  productInfo: { padding: 10 },
  productName: { fontSize: 13, fontWeight: '600', color: Colors.text, marginBottom: 6, minHeight: 36 },
  productFooter: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-end' },
  productPrice: { fontSize: 16, fontWeight: 'bold', color: Colors.primary },
  discountRow: { flexDirection: 'row', alignItems: 'center', marginTop: 2 },
  originalPrice: { fontSize: 11, color: Colors.gray, textDecorationLine: 'line-through', marginRight: 4 },
  productDiscount: { fontSize: 11, color: Colors.success, fontWeight: '600' },
  ratingBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: Colors.secondary, paddingHorizontal: 6, paddingVertical: 2, borderRadius: 4 },
  ratingText: { fontSize: 11, fontWeight: 'bold', color: Colors.white, marginLeft: 2 },
  emptyCategories: { padding: 40 },
  emptyProducts: { width: '100%', padding: 40, alignItems: 'center' },
  emptyText: { fontSize: 16, color: Colors.textSecondary, textAlign: 'center' },
  emptySubtext: { fontSize: 14, color: Colors.gray, textAlign: 'center', marginTop: 8 },
});
