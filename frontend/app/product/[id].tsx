import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  Image,
  ActivityIndicator,
  Alert,
  Dimensions,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter, useLocalSearchParams } from 'expo-router';
import { Colors } from '../../constants/Colors';
import { LOGO_URL } from '../../constants/Logo';
import { useAuthStore } from '../../store/authStore';
import api from '../../utils/api';

const { width } = Dimensions.get('window');

export default function ProductDetail() {
  const router = useRouter();
  const { id } = useLocalSearchParams();
  const { user, isAuthenticated } = useAuthStore();
  const [product, setProduct] = useState<any>(null);
  const [loading, setLoading] = useState(true);
  const [selectedSize, setSelectedSize] = useState('');
  const [selectedColor, setSelectedColor] = useState('');
  const [wishlisted, setWishlisted] = useState(false);
  const [addingToCart, setAddingToCart] = useState(false);

  useEffect(() => {
    fetchProduct();
  }, [id]);

  const fetchProduct = async () => {
    try {
      const response = await api.get(`/products/${id}`);
      setProduct(response.data);
      if (response.data.sizes?.length > 0) setSelectedSize(response.data.sizes[0]);
      if (response.data.colors?.length > 0) setSelectedColor(response.data.colors[0]);
    } catch (error) {
      console.error('Error fetching product:', error);
      Alert.alert('Error', 'Failed to load product');
    } finally {
      setLoading(false);
    }
  };

  const requireLogin = (action: string) => {
    Alert.alert(
      'Login Required',
      `Please register/login to ${action}.`,
      [
        { text: 'Cancel', style: 'cancel' },
        { text: 'Login', onPress: () => router.push('/auth/login') },
        { text: 'Register', onPress: () => router.push('/auth/register') },
      ]
    );
  };

  const handleAddToCart = async () => {
    if (!isAuthenticated) { requireLogin('add items to cart'); return; }
    setAddingToCart(true);
    try {
      await api.post(`/cart/${user?._id}/add`, {
        product_id: id,
        quantity: 1,
        size: selectedSize || null,
        color: selectedColor || null,
      });
      Alert.alert('Added to Cart', `${product.name} has been added to your cart!`, [
        { text: 'Continue Shopping', style: 'cancel' },
        { text: 'View Cart', onPress: () => router.push('/(tabs)/cart') },
      ]);
    } catch (error) {
      Alert.alert('Error', 'Failed to add to cart');
    } finally {
      setAddingToCart(false);
    }
  };

  const handleBuyNow = async () => {
    if (!isAuthenticated) { requireLogin('buy products'); return; }
    setAddingToCart(true);
    try {
      await api.post(`/cart/${user?._id}/add`, {
        product_id: id,
        quantity: 1,
        size: selectedSize || null,
        color: selectedColor || null,
      });
      router.push('/(tabs)/cart');
    } catch (error) {
      Alert.alert('Error', 'Failed to proceed');
    } finally {
      setAddingToCart(false);
    }
  };

  const handleWishlist = async () => {
    if (!isAuthenticated) { requireLogin('add to wishlist'); return; }
    try {
      if (wishlisted) {
        await api.delete(`/wishlist/${user?._id}/remove/${id}`);
        setWishlisted(false);
        Alert.alert('Removed', 'Removed from wishlist');
      } else {
        await api.post(`/wishlist/${user?._id}/add/${id}`);
        setWishlisted(true);
        Alert.alert('Added', 'Added to wishlist!');
      }
    } catch (error) {
      Alert.alert('Error', 'Failed to update wishlist');
    }
  };

  if (loading) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={Colors.primary} />
        </View>
      </SafeAreaView>
    );
  }

  if (!product) {
    return (
      <SafeAreaView style={styles.container}>
        <View style={styles.loadingContainer}>
          <Text style={styles.errorText}>Product not found</Text>
        </View>
      </SafeAreaView>
    );
  }

  const discountedPrice = product.price - (product.price * product.discount / 100);

  return (
    <SafeAreaView style={styles.container}>
      {/* Header */}
      <View style={styles.header}>
        <TouchableOpacity testID="product-back-btn" onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.text} />
        </TouchableOpacity>
        <Image source={{ uri: LOGO_URL }} style={styles.headerLogo} />
        <TouchableOpacity testID="product-wishlist-header-btn" onPress={handleWishlist} style={styles.wishlistBtn}>
          <Ionicons name={wishlisted ? 'heart' : 'heart-outline'} size={24} color={wishlisted ? Colors.error : Colors.text} />
        </TouchableOpacity>
      </View>

      <ScrollView showsVerticalScrollIndicator={false}>
        {/* Product Image */}
        {product.image_url ? (
          <Image source={{ uri: product.image_url }} style={styles.productImage} />
        ) : (
          <View style={styles.productImagePlaceholder}>
            <Ionicons name="image-outline" size={80} color={Colors.gray} />
          </View>
        )}

        {/* Product Info */}
        <View style={styles.infoContainer}>
          {/* Category Badge */}
          <View style={styles.categoryBadge}>
            <Text style={styles.categoryBadgeText}>{product.category}</Text>
          </View>

          <Text style={styles.productName}>{product.name}</Text>

          {/* Rating */}
          {product.rating > 0 && (
            <View style={styles.ratingRow}>
              <View style={styles.ratingBadge}>
                <Ionicons name="star" size={14} color={Colors.white} />
                <Text style={styles.ratingText}>{product.rating}</Text>
              </View>
              <Text style={styles.reviewCount}>({product.review_count} reviews)</Text>
            </View>
          )}

          {/* Price */}
          <View style={styles.priceRow}>
            <Text style={styles.price}>₹{discountedPrice.toFixed(0)}</Text>
            {product.discount > 0 && (
              <>
                <Text style={styles.originalPrice}>₹{product.price}</Text>
                <View style={styles.discountBadge}>
                  <Text style={styles.discountText}>{product.discount}% OFF</Text>
                </View>
              </>
            )}
          </View>

          {/* Sizes */}
          {product.sizes && product.sizes.length > 0 && (
            <View style={styles.optionSection}>
              <Text style={styles.optionLabel}>Size</Text>
              <View style={styles.optionRow}>
                {product.sizes.map((size: string) => (
                  <TouchableOpacity
                    key={size}
                    testID={`size-${size}`}
                    style={[styles.optionChip, selectedSize === size && styles.optionChipActive]}
                    onPress={() => setSelectedSize(size)}
                  >
                    <Text style={[styles.optionChipText, selectedSize === size && styles.optionChipTextActive]}>{size}</Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          )}

          {/* Colors */}
          {product.colors && product.colors.length > 0 && (
            <View style={styles.optionSection}>
              <Text style={styles.optionLabel}>Color</Text>
              <View style={styles.optionRow}>
                {product.colors.map((color: string) => (
                  <TouchableOpacity
                    key={color}
                    testID={`color-${color}`}
                    style={[styles.optionChip, selectedColor === color && styles.optionChipActive]}
                    onPress={() => setSelectedColor(color)}
                  >
                    <Text style={[styles.optionChipText, selectedColor === color && styles.optionChipTextActive]}>{color}</Text>
                  </TouchableOpacity>
                ))}
              </View>
            </View>
          )}

          {/* Description */}
          <View style={styles.descriptionSection}>
            <Text style={styles.descriptionLabel}>Description</Text>
            <Text style={styles.descriptionText}>{product.description}</Text>
          </View>

          {/* Offers */}
          <View style={styles.offersSection}>
            <Text style={styles.offersLabel}>Available Offers</Text>
            <View style={styles.offerItem}>
              <Ionicons name="pricetag" size={16} color={Colors.success} />
              <Text style={styles.offerText}>Premium members get extra 20% off</Text>
            </View>
            <View style={styles.offerItem}>
              <Ionicons name="gift" size={16} color={Colors.primary} />
              <Text style={styles.offerText}>Refer & earn 1% commission up to 9 levels</Text>
            </View>
            <View style={styles.offerItem}>
              <Ionicons name="car" size={16} color={Colors.secondary} />
              <Text style={styles.offerText}>Free shipping on orders above ₹499</Text>
            </View>
          </View>
        </View>
      </ScrollView>

      {/* Bottom Action Buttons */}
      <View style={styles.bottomBar}>
        <TouchableOpacity testID="product-wishlist-btn" style={styles.wishlistBottomBtn} onPress={handleWishlist}>
          <Ionicons name={wishlisted ? 'heart' : 'heart-outline'} size={24} color={wishlisted ? Colors.error : Colors.gray} />
          <Text style={[styles.wishlistBottomText, wishlisted && { color: Colors.error }]}>Wishlist</Text>
        </TouchableOpacity>

        <TouchableOpacity
          testID="product-add-to-cart-btn"
          style={styles.addToCartBtn}
          onPress={handleAddToCart}
          disabled={addingToCart}
        >
          {addingToCart ? (
            <ActivityIndicator size="small" color={Colors.primary} />
          ) : (
            <>
              <Ionicons name="cart-outline" size={20} color={Colors.primary} />
              <Text style={styles.addToCartText}>Add to Cart</Text>
            </>
          )}
        </TouchableOpacity>

        <TouchableOpacity
          testID="product-buy-now-btn"
          style={styles.buyNowBtn}
          onPress={handleBuyNow}
          disabled={addingToCart}
        >
          <Ionicons name="flash" size={20} color={Colors.white} />
          <Text style={styles.buyNowText}>Buy Now</Text>
        </TouchableOpacity>
      </View>
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.white },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  errorText: { fontSize: 16, color: Colors.textSecondary },
  header: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'center', paddingHorizontal: 16, paddingVertical: 12, borderBottomWidth: 1, borderBottomColor: Colors.border },
  backBtn: { width: 40, height: 40, borderRadius: 20, backgroundColor: Colors.lightGray, justifyContent: 'center', alignItems: 'center' },
  headerLogo: { width: 40, height: 40, resizeMode: 'contain' },
  wishlistBtn: { width: 40, height: 40, borderRadius: 20, backgroundColor: Colors.lightGray, justifyContent: 'center', alignItems: 'center' },
  productImage: { width: width, height: width * 0.85, resizeMode: 'cover' },
  productImagePlaceholder: { width: width, height: width * 0.85, backgroundColor: Colors.lightGray, justifyContent: 'center', alignItems: 'center' },
  infoContainer: { padding: 20 },
  categoryBadge: { backgroundColor: Colors.lightGray, paddingHorizontal: 12, paddingVertical: 4, borderRadius: 12, alignSelf: 'flex-start', marginBottom: 12 },
  categoryBadgeText: { fontSize: 12, color: Colors.textSecondary, fontWeight: '600' },
  productName: { fontSize: 22, fontWeight: 'bold', color: Colors.text, marginBottom: 8, lineHeight: 30 },
  ratingRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 12 },
  ratingBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: Colors.secondary, paddingHorizontal: 8, paddingVertical: 4, borderRadius: 6 },
  ratingText: { fontSize: 13, fontWeight: 'bold', color: Colors.white, marginLeft: 4 },
  reviewCount: { fontSize: 13, color: Colors.textSecondary, marginLeft: 8 },
  priceRow: { flexDirection: 'row', alignItems: 'center', marginBottom: 20 },
  price: { fontSize: 28, fontWeight: 'bold', color: Colors.primary, marginRight: 12 },
  originalPrice: { fontSize: 18, color: Colors.gray, textDecorationLine: 'line-through', marginRight: 8 },
  discountBadge: { backgroundColor: '#E8F5E9', paddingHorizontal: 8, paddingVertical: 4, borderRadius: 6 },
  discountText: { fontSize: 13, fontWeight: 'bold', color: Colors.success },
  optionSection: { marginBottom: 20 },
  optionLabel: { fontSize: 16, fontWeight: '600', color: Colors.text, marginBottom: 10 },
  optionRow: { flexDirection: 'row', flexWrap: 'wrap', gap: 8 },
  optionChip: { paddingHorizontal: 18, paddingVertical: 10, borderRadius: 8, borderWidth: 1.5, borderColor: Colors.border, backgroundColor: Colors.white },
  optionChipActive: { borderColor: Colors.primary, backgroundColor: Colors.primary + '10' },
  optionChipText: { fontSize: 14, color: Colors.text, fontWeight: '500' },
  optionChipTextActive: { color: Colors.primary, fontWeight: '700' },
  descriptionSection: { marginBottom: 20 },
  descriptionLabel: { fontSize: 16, fontWeight: '600', color: Colors.text, marginBottom: 8 },
  descriptionText: { fontSize: 14, color: Colors.textSecondary, lineHeight: 22 },
  offersSection: { marginBottom: 20, backgroundColor: Colors.lightGray, padding: 16, borderRadius: 12 },
  offersLabel: { fontSize: 16, fontWeight: '600', color: Colors.text, marginBottom: 12 },
  offerItem: { flexDirection: 'row', alignItems: 'center', marginBottom: 10 },
  offerText: { fontSize: 13, color: Colors.text, marginLeft: 10, flex: 1 },
  bottomBar: { flexDirection: 'row', paddingHorizontal: 12, paddingVertical: 12, borderTopWidth: 1, borderTopColor: Colors.border, backgroundColor: Colors.white, gap: 8 },
  wishlistBottomBtn: { alignItems: 'center', justifyContent: 'center', paddingHorizontal: 12, paddingVertical: 8 },
  wishlistBottomText: { fontSize: 10, color: Colors.gray, marginTop: 2, fontWeight: '500' },
  addToCartBtn: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', height: 52, borderRadius: 12, borderWidth: 2, borderColor: Colors.primary, backgroundColor: Colors.white },
  addToCartText: { fontSize: 15, fontWeight: '700', color: Colors.primary, marginLeft: 6 },
  buyNowBtn: { flex: 1, flexDirection: 'row', alignItems: 'center', justifyContent: 'center', height: 52, borderRadius: 12, backgroundColor: Colors.primary },
  buyNowText: { fontSize: 15, fontWeight: '700', color: Colors.white, marginLeft: 6 },
});
