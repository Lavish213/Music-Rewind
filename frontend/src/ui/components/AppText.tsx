import React, { ReactNode } from "react";
import { Text, StyleSheet, TextStyle } from "react-native";
import { colors, typography } from "../tokens";

type Variant = "title" | "body" | "muted" | "caption";

interface AppTextProps {
  children: ReactNode;
  variant?: Variant;
  style?: TextStyle;
}

export function AppText({
  children,
  variant = "body",
  style,
}: AppTextProps) {
  return (
    <Text style={[styles.base, styles[variant], style]}>
      {children}
    </Text>
  );
}

const styles = StyleSheet.create({
  base: {
    color: colors.text.primary,
  },

  title: {
    fontSize: typography.size.xl,
    fontWeight: typography.weight.bold,
  },

  body: {
    fontSize: typography.size.md,
    lineHeight: typography.lineHeight.relaxed * typography.size.md,
  },

  muted: {
    fontSize: typography.size.sm,
    color: colors.text.muted,
  },

  caption: {
    fontSize: typography.size.xs,
    color: colors.text.secondary,
  },
});