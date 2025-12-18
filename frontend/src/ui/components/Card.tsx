import React, { ReactNode } from "react";
import { View, StyleSheet } from "react-native";
import { colors, spacing, radius, shadows } from "../tokens";

interface CardProps {
  children: ReactNode;
}

export function Card({ children }: CardProps) {
  return <View style={styles.card}>{children}</View>;
}

const styles = StyleSheet.create({
  card: {
    backgroundColor: colors.background.card,
    borderRadius: radius.lg,
    padding: spacing.lg,
    marginBottom: spacing.md,
    ...shadows.card,
  },
});