import React, { useState, useEffect } from 'react';
import {
  View,
  Text,
  StyleSheet,
  ScrollView,
  TouchableOpacity,
  ActivityIndicator,
} from 'react-native';
import { SafeAreaView } from 'react-native-safe-area-context';
import { Ionicons } from '@expo/vector-icons';
import { useRouter } from 'expo-router';
import { Colors } from '../constants/Colors';
import { useAuthStore } from '../store/authStore';
import api from '../utils/api';

const STATUS_STEPS = ['placed', 'confirmed', 'shipped', 'delivered'];

export default function Orders() {
  const router = useRouter();
  const user = useAuthStore((state) => state.user);
  const [orders, setOrders] = useState<any[]>([]);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    if (user?._id) fetchOrders();
  }, [user]);

  const fetchOrders = async () => {
    try {
      const response = await api.get(`/orders/${user?._id}`);
      setOrders(response.data.orders || []);
    } catch (error) {
      console.error('Error fetching orders:', error);
    } finally {
      setLoading(false);
    }
  };

  const getStatusIndex = (status: string) => {
    const index = STATUS_STEPS.indexOf(status);
    return index >= 0 ? index : 0;
  };

  const getStatusColor = (status: string) => {
    switch (status) {
      case 'delivered': return Colors.success;
      case 'cancelled': return Colors.error;
      case 'shipped': return '#2196F3';
      default: return Colors.primary;
    }
  };

  const formatDate = (dateStr: string) => {
    return new Date(dateStr).toLocaleDateString('en-IN', {
      day: 'numeric',
      month: 'short',
      year: 'numeric',
    });
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

  return (
    <SafeAreaView style={styles.container}>
      <View style={styles.header}>
        <TouchableOpacity testID="orders-back-btn" onPress={() => router.back()} style={styles.backBtn}>
          <Ionicons name="arrow-back" size={24} color={Colors.text} />
        </TouchableOpacity>
        <Text style={styles.headerTitle}>My Orders</Text>
        <View style={{ width: 40 }} />
      </View>

      {orders.length > 0 ? (
        <ScrollView contentContainerStyle={styles.content} showsVerticalScrollIndicator={false}>
          {orders.map((order: any) => (
            <View key={order.order_id} style={styles.orderCard}>
              <View style={styles.orderHeader}>
                <View>
                  <Text style={styles.orderId}>#{order.order_id}</Text>
                  <Text style={styles.orderDate}>{formatDate(order.created_at)}</Text>
                </View>
                <View style={[styles.statusBadge, { backgroundColor: getStatusColor(order.order_status) + '20' }]}>
                  <Text style={[styles.statusText, { color: getStatusColor(order.order_status) }]}>
                    {order.order_status.toUpperCase()}
                  </Text>
                </View>
              </View>

              {/* Order Status Tracker */}
              {order.order_status !== 'cancelled' && (
                <View style={styles.tracker}>
                  {STATUS_STEPS.map((step, index) => (
                    <View key={step} style={styles.trackerStep}>
                      <View style={[
                        styles.trackerDot,
                        index <= getStatusIndex(order.order_status) && styles.trackerDotActive,
                      ]}>
                        {index <= getStatusIndex(order.order_status) && (
                          <Ionicons name="checkmark" size={12} color={Colors.white} />
                        )}
                      </View>
                      {index < STATUS_STEPS.length - 1 && (
                        <View style={[
                          styles.trackerLine,
                          index < getStatusIndex(order.order_status) && styles.trackerLineActive,
                        ]} />
                      )}
                      <Text style={[
                        styles.trackerLabel,
                        index <= getStatusIndex(order.order_status) && styles.trackerLabelActive,
                      ]}>
                        {step.charAt(0).toUpperCase() + step.slice(1)}
                      </Text>
                    </View>
                  ))}
                </View>
              )}

              {/* Items */}
              <View style={styles.orderItems}>
                {order.items?.map((item: any, idx: number) => (
                  <View key={idx} style={styles.orderItem}>
                    <View style={styles.orderItemIcon}>
                      <Ionicons name="cube-outline" size={20} color={Colors.gray} />
                    </View>
                    <View style={styles.orderItemInfo}>
                      <Text style={styles.orderItemName} numberOfLines={1}>
                        {item.product_name || 'Product'}
                      </Text>
                      <Text style={styles.orderItemDetails}>
                        Qty: {item.quantity} {item.size ? `| ${item.size}` : ''} {item.color ? `| ${item.color}` : ''}
                      </Text>
                    </View>
                    <Text style={styles.orderItemPrice}>₹{(item.price * item.quantity).toFixed(0)}</Text>
                  </View>
                ))}
              </View>

              <View style={styles.orderFooter}>
                <Text style={styles.totalLabel}>Total Amount</Text>
                <Text style={styles.totalAmount}>₹{order.total?.toFixed(2)}</Text>
              </View>
            </View>
          ))}
        </ScrollView>
      ) : (
        <View style={styles.emptyContainer}>
          <Ionicons name="receipt-outline" size={80} color={Colors.gray} />
          <Text style={styles.emptyText}>No orders yet</Text>
          <Text style={styles.emptySubtext}>Start shopping to see your orders here</Text>
        </View>
      )}
    </SafeAreaView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: Colors.lightGray,
  },
  loadingContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
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
  orderCard: {
    backgroundColor: Colors.white,
    borderRadius: 12,
    padding: 16,
    marginBottom: 16,
  },
  orderHeader: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    marginBottom: 16,
  },
  orderId: {
    fontSize: 16,
    fontWeight: 'bold',
    color: Colors.text,
  },
  orderDate: {
    fontSize: 13,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  statusBadge: {
    paddingHorizontal: 12,
    paddingVertical: 6,
    borderRadius: 12,
  },
  statusText: {
    fontSize: 12,
    fontWeight: 'bold',
  },
  tracker: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'flex-start',
    marginBottom: 16,
    paddingHorizontal: 4,
  },
  trackerStep: {
    alignItems: 'center',
    flex: 1,
  },
  trackerDot: {
    width: 24,
    height: 24,
    borderRadius: 12,
    backgroundColor: Colors.border,
    justifyContent: 'center',
    alignItems: 'center',
    marginBottom: 6,
  },
  trackerDotActive: {
    backgroundColor: Colors.success,
  },
  trackerLine: {
    position: 'absolute',
    top: 12,
    left: '60%',
    right: '-40%',
    height: 2,
    backgroundColor: Colors.border,
  },
  trackerLineActive: {
    backgroundColor: Colors.success,
  },
  trackerLabel: {
    fontSize: 10,
    color: Colors.gray,
    textAlign: 'center',
  },
  trackerLabelActive: {
    color: Colors.text,
    fontWeight: '600',
  },
  orderItems: {
    borderTopWidth: 1,
    borderTopColor: Colors.border,
    paddingTop: 12,
    marginBottom: 12,
  },
  orderItem: {
    flexDirection: 'row',
    alignItems: 'center',
    paddingVertical: 8,
  },
  orderItemIcon: {
    width: 36,
    height: 36,
    borderRadius: 8,
    backgroundColor: Colors.lightGray,
    justifyContent: 'center',
    alignItems: 'center',
  },
  orderItemInfo: {
    flex: 1,
    marginLeft: 12,
  },
  orderItemName: {
    fontSize: 14,
    fontWeight: '600',
    color: Colors.text,
  },
  orderItemDetails: {
    fontSize: 12,
    color: Colors.textSecondary,
    marginTop: 2,
  },
  orderItemPrice: {
    fontSize: 14,
    fontWeight: 'bold',
    color: Colors.text,
  },
  orderFooter: {
    flexDirection: 'row',
    justifyContent: 'space-between',
    alignItems: 'center',
    borderTopWidth: 1,
    borderTopColor: Colors.border,
    paddingTop: 12,
  },
  totalLabel: {
    fontSize: 14,
    color: Colors.textSecondary,
    fontWeight: '500',
  },
  totalAmount: {
    fontSize: 20,
    fontWeight: 'bold',
    color: Colors.primary,
  },
  emptyContainer: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
    paddingHorizontal: 40,
  },
  emptyText: {
    fontSize: 20,
    fontWeight: 'bold',
    color: Colors.text,
    marginTop: 24,
  },
  emptySubtext: {
    fontSize: 14,
    color: Colors.textSecondary,
    marginTop: 8,
    textAlign: 'center',
  },
});
