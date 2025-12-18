import React from "react";
import { Pressable, Text, StyleSheet } from "react-native";
import { colors, spacing, radius, typography } from "../tokens";

type ButtonVariant = "primary" | "secondary" | "ghost";

interface ButtonProps {
  label: string;
  onPress: () => void;
  variant?: ButtonVariant;
  disabled?: boolean;
}

export function Button({
  label,
  onPress,
  variant = "primary",
  disabled = false,
}: ButtonProps) {
  return (
    <Pressable
      onPress={onPress}
      disabled={disabled}
      style={({ pressed }) => [
        styles.base,
        styles[variant],
        pressed && styles.pressed,
        disabled && styles.disabled,
      ]}
    >
      <Text style={[styles.text, styles[`text_${variant}`]]}>
        {label}
      </Text>
    </Pressable>
  );
}

const styles = StyleSheet.create({
  base: {
    paddingVertical: spacing.md,
    paddingHorizontal: spacing.lg,
    borderRadius: radius.lg,
    alignItems: "center",
    justifyContent: "center",
  },

  pressed: {
    opacity: 0.85,
  },

  disabled: {
    backgroundColor: colors.state.disabled,
  },

  primary: {
    backgroundColor: colors.brand.primary,
  },

  secondary: {
    backgroundColor: colors.background.cardSoft,
    borderWidth: 1,
    borderColor: colors.border.light,
  },

  ghost: {
    backgroundColor: "transparent",
  },

  text: {
    fontSize: typography.size.md,
    fontWeight: typography.weight.semibold,
  },

  text_primary: {
    color: colors.text.inverse,
  },

  text_secondary: {
    color: colors.text.primary,
  },

  text_ghost: {
    color: colors.brand.primary,
  },
});