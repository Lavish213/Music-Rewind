// LOCATION: src/screens/TimelineScreen.tsx
import React from "react";
import { ScrollView, StyleSheet } from "react-native";
import { TimelineHeader } from "../../frontend/src/ui/components/timeline/TimelineHeader";
import { YearSelector } from "../../frontend/src/ui/components/timeline/YearSelector";
import { SongMemoryCard } from "../../frontend/src/ui/components/timeline/SongMemoryCard";
import { colors, spacing } from "../../frontend/src/ui/tokens";
export function TimelineScreen() {
  return (
    <ScrollView style={styles.container}>
      <TimelineHeader />
      <YearSelector />
      <SongMemoryCard />
      <SongMemoryCard />
    </ScrollView>
  );
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
backgroundColor: colors.background.app,
  },
});

