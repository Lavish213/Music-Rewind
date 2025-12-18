import React from "react";
import { View, StyleSheet, Image } from "react-native";

import { AppText } from "..";
import { colors, spacing, radius, shadows } from "../../tokens";
export function SongMemoryCard() {
  return (
    <View style={styles.card}>
      <Image
        source={{ uri: "https://via.placeholder.com/300" }}
        style={styles.cover}
      />

      <AppText variant="title" style={styles.title}>
        Electric Feel
      </AppText>
      <AppText variant="muted">MGMT • 2007</AppText>

      <AppText variant="body" style={styles.context}>
        You played this most during late-night drives.
      </AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.background.card,
    marginHorizontal: spacing.lg,
    marginBottom: spacing.md,
    borderRadius: radius.lg,
    padding: spacing.lg,
    ...shadows.card,
  },
  cover: {
    width: "100%",
    height: 140,
    borderRadius: radius.md,
    marginBottom: spacing.md,
    backgroundColor: colors.background.cardSoft,
  },
  title: {
    marginBottom: spacing.xs,
  },
  context: {
    marginTop: spacing.sm,
    color: colors.text.secondary,
  },
});