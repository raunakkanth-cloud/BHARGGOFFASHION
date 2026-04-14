import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  FlatList,
  TouchableOpacity,
  TextInput,
  ActivityIndicator,
  Dimensions,
  Image,
  ScrollView,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { Colors } from '../../constants/Colors';
import { LOGO_URL } from '../../constants/Logo';
import api from '../../utils/api';

const { width } = Dimensions.get('window');

export default function Products() {
  const [products, setProducts] = useState([]);
  const [loading, setLoading] = useState(true);
  const [search, setSearch] = useState('');
  const [selectedCategory, setSelectedCategory] = useState('');
  const [categories, setCategories] = useState([]);

  useEffect(() => {
    fetchCategories();
    fetchProducts();
  }, []);

  const fetchCategories = async () => {
    try {
      const response = await api.get('/categories');
      setCategories(response.data.categories || []);
    } catch (error) {
      console.error('Error fetching categories:', error);
    }
  };

  const fetchProducts = async () => {
    setLoading(true);
    try {
      const params: any = {};
      if (search) params.search = search;
      if (selectedCategory) params.category = selectedCategory;
      
      const response = await api.get('/products', { params });
      setProducts(response.data.products || []);
    } catch (error) {
      console.error('Error fetching products:', error);
    } finally {
      setLoading(false);
    }
  };

  useEffect(() => {
    const timer = setTimeout(() => {
      fetchProducts();
    }, 500);
    return () => clearTimeout(timer);
  }, [search, selectedCategory]);

  const renderProduct = ({ item }: any) => (
    <TouchableOpacity testID={`product-card-${item._id}`} style={styles.productCard}>
      {item.image_url ? (
        <Image source={{ uri: item.image_url }} style={styles.productImage} />
      ) : (
        <View style={styles.productImagePlaceholder}>
          <Ionicons name="image-outline" size={48} color={Colors.gray} />
        </View>
      )}
      <View style={styles.productInfo}>
        <Text style={styles.productName} numberOfLines={2}>{item.name}</Text>
        <Text style={styles.productCategory}>{item.category}</Text>
        <View style={styles.productFooter}>
          <View>
            <Text style={styles.productPrice}>₹{(item.price - (item.price * item.discount / 100)).toFixed(0)}</Text>
            {item.discount > 0 && (
              <View style={styles.discountRow}>
                <Text style={styles.originalPrice}>₹{item.price}</Text>
                <Text style={styles.productDiscount}>{item.discount}% OFF</Text>
              </View>
            )}
          </View>
          {item.rating > 0 && (
            <View style={styles.ratingBadge}>
              <Ionicons name="star" size={12} color={Colors.white} />
              <Text style={styles.ratingText}>{item.rating}</Text>
            </View>
          )}
        </View>
      </View>
    </TouchableOpacity>
  );

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <Image source={{ uri: LOGO_URL }} style={styles.headerLogo} />
        <Text style={styles.title}>Products</Text>
      </View>

      <View style={styles.searchContainer}>
        <Ionicons name="search" size={20} color={Colors.gray} style={styles.searchIcon} />
        <TextInput
          testID="products-search-input"
          style={styles.searchInput}
          placeholder="Search products..."
          placeholderTextColor={Colors.gray}
          value={search}
          onChangeText={setSearch}
        />
        {search.length > 0 && (
          <TouchableOpacity onPress={() => setSearch('')}>
            <Ionicons name="close-circle" size={20} color={Colors.gray} />
          </TouchableOpacity>
        )}
      </View>

      {categories.length > 0 && (
        <ScrollableCategories
          categories={categories}
          selectedCategory={selectedCategory}
          onSelect={setSelectedCategory}
        />
      )}

      {loading ? (
        <View style={styles.loadingContainer}>
          <ActivityIndicator size="large" color={Colors.primary} />
        </View>
      ) : products.length > 0 ? (
        <FlatList
          data={products}
          renderItem={renderProduct}
          keyExtractor={(item: any) => item._id}
          numColumns={2}
          contentContainerStyle={styles.productsList}
          showsVerticalScrollIndicator={false}
        />
      ) : (
        <View style={styles.emptyContainer}>
          <Ionicons name="cube-outline" size={64} color={Colors.gray} />
          <Text style={styles.emptyText}>No products found</Text>
          <Text style={styles.emptySubtext}>Try a different search or category</Text>
        </View>
      )}
    </SafeAreaView>
  );
}

function ScrollableCategories({ categories, selectedCategory, onSelect }: any) {
  return (
    <View style={styles.categoriesContainer}>
      <TouchableOpacity
        testID="category-all-btn"
        style={[styles.categoryChip, !selectedCategory && styles.categoryChipActive]}
        onPress={() => onSelect('')}
      >
        <Text style={[styles.categoryChipText, !selectedCategory && styles.categoryChipTextActive]}>All</Text>
      </TouchableOpacity>
      {categories.map((category: string, index: number) => (
        <TouchableOpacity
          key={index}
          testID={`category-${category}-btn`}
          style={[styles.categoryChip, selectedCategory === category && styles.categoryChipActive]}
          onPress={() => onSelect(category)}
        >
          <Text style={[styles.categoryChipText, selectedCategory === category && styles.categoryChipTextActive]}>{category}</Text>
        </TouchableOpacity>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: Colors.white },
  header: { flexDirection: 'row', alignItems: 'center', paddingHorizontal: 16, paddingVertical: 12 },
  headerLogo: { width: 44, height: 44, resizeMode: 'contain', marginRight: 12 },
  title: { fontSize: 28, fontWeight: 'bold', color: Colors.text },
  searchContainer: { flexDirection: 'row', alignItems: 'center', marginHorizontal: 20, marginBottom: 16, paddingHorizontal: 16, height: 48, backgroundColor: Colors.lightGray, borderRadius: 12 },
  searchIcon: { marginRight: 12 },
  searchInput: { flex: 1, fontSize: 16, color: Colors.text },
  categoriesContainer: { flexDirection: 'row', paddingHorizontal: 20, marginBottom: 16, flexWrap: 'wrap' },
  categoryChip: { paddingHorizontal: 16, paddingVertical: 8, borderRadius: 20, backgroundColor: Colors.lightGray, marginRight: 8, marginBottom: 8 },
  categoryChipActive: { backgroundColor: Colors.primary },
  categoryChipText: { fontSize: 14, color: Colors.text, fontWeight: '500' },
  categoryChipTextActive: { color: Colors.white },
  loadingContainer: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  productsList: { paddingHorizontal: 12, paddingBottom: 20 },
  productCard: { width: (width - 48) / 2, margin: 8, backgroundColor: Colors.white, borderRadius: 12, overflow: 'hidden', borderWidth: 1, borderColor: Colors.border },
  productImage: { width: '100%', height: 160 },
  productImagePlaceholder: { width: '100%', height: 160, backgroundColor: Colors.lightGray, justifyContent: 'center', alignItems: 'center' },
  productInfo: { padding: 10 },
  productName: { fontSize: 13, fontWeight: '600', color: Colors.text, marginBottom: 4, minHeight: 36 },
  productCategory: { fontSize: 11, color: Colors.textSecondary, marginBottom: 6 },
  productFooter: { flexDirection: 'row', justifyContent: 'space-between', alignItems: 'flex-end' },
  productPrice: { fontSize: 16, fontWeight: 'bold', color: Colors.primary },
  discountRow: { flexDirection: 'row', alignItems: 'center', marginTop: 2 },
  originalPrice: { fontSize: 11, color: Colors.gray, textDecorationLine: 'line-through', marginRight: 4 },
  productDiscount: { fontSize: 11, color: Colors.success, fontWeight: '600' },
  ratingBadge: { flexDirection: 'row', alignItems: 'center', backgroundColor: Colors.secondary, paddingHorizontal: 6, paddingVertical: 2, borderRadius: 4 },
  ratingText: { fontSize: 11, fontWeight: 'bold', color: Colors.white, marginLeft: 2 },
  emptyContainer: { flex: 1, justifyContent: 'center', alignItems: 'center', paddingHorizontal: 40 },
  emptyText: { fontSize: 18, fontWeight: '600', color: Colors.text, marginTop: 16, textAlign: 'center' },
  emptySubtext: { fontSize: 14, color: Colors.textSecondary, marginTop: 8, textAlign: 'center' },
});
