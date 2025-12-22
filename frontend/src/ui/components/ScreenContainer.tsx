import React from "react";
import { View, StyleSheet } from "react-native";
import { colors } from "../tokens/colors";

type Props = {
  children: React.ReactNode;
};

export function ScreenContainer({ children }: Props) {
  return <View style={styles.container}>{children}</View>;
}

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background.card,
    padding: 16,
  },
});