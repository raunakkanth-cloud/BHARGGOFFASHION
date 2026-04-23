import { create } from 'zustand';
import AsyncStorage from '@react-native-async-storage/async-storage';

interface User {
  _id: string;
  id?: string;
  email: string;
  name: string;
  referral_id: string;
  sponsor_id?: string;
  subscription_status: boolean;
  wallet_balance: number;
  total_commission_earned: number;
  level: number;
  mobile?: string;
  address?: string;
  pincode?: string;
  created_at?: string;
}

// Normalize user object to always have _id
function normalizeUser(user: any): User {
  const normalized = { ...user };
  if (!normalized._id && normalized.id) {
    normalized._id = normalized.id;
  }
  if (!normalized._id && !normalized.id) {
    normalized._id = '';
  }
  return normalized;
}

interface AuthState {
  user: User | null;
  token: string | null;
  isAuthenticated: boolean;
  setUser: (user: any) => void;
  setToken: (token: string) => void;
  logout: () => void;
  loadAuth: () => Promise<void>;
}

export const useAuthStore = create<AuthState>((set) => ({
  user: null,
  token: null,
  isAuthenticated: false,
  setUser: (user) => {
    const normalized = normalizeUser(user);
    set({ user: normalized, isAuthenticated: true });
  },
  setToken: async (token) => {
    await AsyncStorage.setItem('auth_token', token);
    set({ token });
  },
  logout: async () => {
    await AsyncStorage.removeItem('auth_token');
    await AsyncStorage.removeItem('user_data');
    set({ user: null, token: null, isAuthenticated: false });
  },
  loadAuth: async () => {
    try {
      const token = await AsyncStorage.getItem('auth_token');
      const userData = await AsyncStorage.getItem('user_data');
      if (token && userData) {
        const user = normalizeUser(JSON.parse(userData));
        set({ token, user, isAuthenticated: true });
      }
    } catch (error) {
      console.error('Error loading auth:', error);
    }
  },
}));
