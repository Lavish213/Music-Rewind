import { Image } from 'expo-image';
import { ActivityIndicator, StyleSheet } from 'react-native';
import { useEffect, useState } from 'react';

import ParallaxScrollView from '@/components/parallax-scroll-view';
import { ThemedText } from '@/components/themed-text';
import { ThemedView } from '@/components/themed-view';

import { fetchRewindSummary, RewindSummary } from '../../src/api/rewind';

export default function HomeScreen() {
  const [data, setData] = useState<RewindSummary | null>(null);
  const [error, setError] = useState<string | null>(null);

  useEffect(() => {
  let mounted = true;

  fetchRewindSummary()
    .then((res: RewindSummary) => {
      if (mounted) setData(res);
    })
    .catch((err: unknown) => {
      console.error(err);
      if (mounted) setError('Unable to load rewind');
    });

  return () => {
    mounted = false;
  };
}, []);

  if (error) {
    return (
      <ThemedView style={styles.center}>
        <ThemedText type="subtitle">{error}</ThemedText>
      </ThemedView>
    );
  }

  if (!data) {
    return (
      <ThemedView style={styles.center}>
        <ActivityIndicator size="large" />
      </ThemedView>
    );
  }

  return (
    <ParallaxScrollView
      headerBackgroundColor={{ light: '#A1CEDC', dark: '#1D3D47' }}
      headerImage={
        <Image
          source={require('@/assets/images/partial-react-logo.png')}
          style={styles.reactLogo}
          contentFit="contain"
        />
      }
    >
      <ThemedView style={styles.section}>
        <ThemedText type="title">Welcome, {data.user.name}</ThemedText>
      </ThemedView>

      <ThemedView style={styles.section}>
        <ThemedText type="subtitle">Your Rewind</ThemedText>
        <ThemedText>Top Artist: {data.topArtist}</ThemedText>
        <ThemedText>Top Song: {data.topSong}</ThemedText>
        <ThemedText>
          Minutes Played: {data.minutesPlayed.toLocaleString()}
        </ThemedText>
      </ThemedView>
    </ParallaxScrollView>
  );
}

const styles = StyleSheet.create({
  section: {
    gap: 8,
    marginBottom: 16,
  },
  center: {
    flex: 1,
    justifyContent: 'center',
    alignItems: 'center',
  },
  reactLogo: {
    height: 180,
    width: 300,
    position: 'absolute',
    bottom: 0,
    left: 0,
  },
});