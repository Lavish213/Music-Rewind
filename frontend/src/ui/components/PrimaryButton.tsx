import React from "react";
import { Pressable, Text } from "react-native";
import { colors, radius, spacing } from "../tokens";

export function PrimaryButton({
  title,
  onPress,
}: {
  title: string;
  onPress: () => void;
}) {
  return (
    <Pressable
      onPress={onPress}
      style={{
        backgroundColor: colors.brand.primary,
        paddingVertical: spacing.md,
        borderRadius: radius.md,
        alignItems: "center",
      }}
    >
      <Text style={{ color: "white", fontWeight: "600" }}>
        {title}
      </Text>
    </Pressable>
  );
}
