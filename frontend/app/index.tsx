import React, { useEffect, useRef } from 'react';
import { View, Text, StyleSheet, Animated, Dimensions, Image } from 'react-native';
import { useRouter } from 'expo-router';
import { Colors } from '../constants/Colors';
import { LOGO_URL } from '../constants/Logo';

const { width } = Dimensions.get('window');

export default function Index() {
  const router = useRouter();
  const logoScale = useRef(new Animated.Value(0.3)).current;
  const logoOpacity = useRef(new Animated.Value(0)).current;
  const textOpacity = useRef(new Animated.Value(0)).current;
  const taglineOpacity = useRef(new Animated.Value(0)).current;

  useEffect(() => {
    Animated.sequence([
      Animated.parallel([
        Animated.spring(logoScale, {
          toValue: 1,
          tension: 10,
          friction: 3,
          useNativeDriver: true,
        }),
        Animated.timing(logoOpacity, {
          toValue: 1,
          duration: 600,
          useNativeDriver: true,
        }),
      ]),
      Animated.timing(textOpacity, {
        toValue: 1,
        duration: 400,
        useNativeDriver: true,
      }),
      Animated.timing(taglineOpacity, {
        toValue: 1,
        duration: 400,
        useNativeDriver: true,
      }),
    ]).start();

    // Always go to home - guest browsing allowed
    const timer = setTimeout(() => {
      router.replace('/(tabs)/home');
    }, 2500);

    return () => clearTimeout(timer);
  }, []);

  return (
    <View style={styles.container}>
      <View style={styles.topStrip} />

      <View style={styles.content}>
        <Animated.View
          style={[
            styles.logoContainer,
            { transform: [{ scale: logoScale }], opacity: logoOpacity },
          ]}
        >
          <Image source={{ uri: LOGO_URL }} style={styles.logoImage} />
        </Animated.View>

        <Animated.View style={{ opacity: textOpacity }}>
          <Text style={styles.tagline}>A Brand with Ethical, Durable & Stylish Clothing</Text>
        </Animated.View>
      </View>

      <View style={styles.bottomStrip} />

      <View style={styles.footer}>
        <Text style={styles.footerText}>Bharggo FFashion India Pvt. Ltd.</Text>
      </View>
    </View>
  );
}

const styles = StyleSheet.create({
  container: { flex: 1, backgroundColor: '#0A0A0A' },
  topStrip: { height: 4, backgroundColor: Colors.primary },
  content: { flex: 1, justifyContent: 'center', alignItems: 'center' },
  logoContainer: { marginBottom: 16 },
  logoImage: { width: width * 0.6, height: width * 0.6, resizeMode: 'contain' },
  tagline: { fontSize: 13, color: '#999', textAlign: 'center', letterSpacing: 1, paddingHorizontal: 40 },
  bottomStrip: { height: 4, backgroundColor: Colors.secondary },
  footer: { padding: 16, alignItems: 'center' },
  footerText: { fontSize: 12, color: '#666', letterSpacing: 1 },
});
