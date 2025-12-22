import React from "react";
import { View, StyleSheet, Image } from "react-native";
import { AppText } from "../AppText";
import { colors, spacing, radius, shadows } from "../../tokens";
type SongMemoryCardProps = {
  title: string;
  artist: string;
  year: number;
  note: string;
  imageUrl?: string;
};

export function SongMemoryCard({
  title,
  artist,
  year,
  note,
  imageUrl,
}: SongMemoryCardProps) {
  return (
    <View style={styles.card}>
      <Image
        source={{
          uri: imageUrl ?? "https://via.placeholder.com/300",
        }}
        style={styles.cover}
      />

      <AppText variant="title" style={styles.title}>
        {title}
      </AppText>

      <AppText variant="muted">
        {artist} • {year}
      </AppText>

      <AppText variant="body" style={styles.context}>
        {note}
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