import React from "react";
import { View, StyleSheet } from "react-native";

import { AppText } from "../AppText";
import { colors, spacing } from "../../tokens";


export function TimelineHeader() {
  return (
    <View style={styles.container}>
      <AppText variant="title">Relive your music years</AppText>

      <AppText variant="muted" style={styles.subtitle}>
        Moments by year and mood
      </AppText>
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    paddingHorizontal: spacing.lg,
    paddingTop: spacing.lg,
    paddingBottom: spacing.md,
   backgroundColor: colors.background.app,
  },
  subtitle: {
    marginTop: spacing.xs,
  },
});