import React from "react";
import { View, StyleSheet } from "react-native";
import { colors } from "../tokens";

type Props = {
  children: React.ReactNode;
};

export function ScreenContainer({ children }: Props) {
  return <View style={styles.container}>{children}</View>;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background.surface,
    padding: 16,
  },
});