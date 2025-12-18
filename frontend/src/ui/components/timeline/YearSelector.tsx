// LOCATION: src/components/timeline/YearSelector.tsx
import React, { useState } from "react";
import { View, ScrollView, Pressable, StyleSheet } from "react-native";
import { AppText } from "../AppText";
import { colors, spacing, radius } from "../../tokens";

const YEARS = ["2008", "2010", "2012", "2014", "2016", "2018", "2020", "2022"];

export function YearSelector() {
  const [active, setActive] = useState<string>(YEARS[0]);

  return (
    <View style={styles.wrap}>
      <ScrollView
        horizontal
        showsHorizontalScrollIndicator={false}
        contentContainerStyle={styles.row}
      >
        {YEARS.map((y) => {
          const isActive = y === active;
          return (
            <Pressable
              key={y}
              onPress={() => setActive(y)}
              style={[
                styles.chip,
                isActive && styles.chipActive,
              ]}
            >
              <AppText
                variant="body"
                style={{ color: isActive ? colors.text.inverse : colors.text.primary }}
              >
                {y}
              </AppText>
            </Pressable>
          );
        })}
      </ScrollView>
    </View>
  );
}

const styles = StyleSheet.create({
  wrap: {
backgroundColor: colors.background.card,
    paddingVertical: spacing.sm,
  },
  row: {
    paddingHorizontal: spacing.lg,
    gap: spacing.sm,
  },
  chip: {
    paddingVertical: spacing.xs,
    paddingHorizontal: spacing.md,
  borderRadius: radius.lg,
    backgroundColor: colors.background.cardSoft,
    borderWidth: 1,
    borderColor: colors.border.light,
  },
  chipActive: {
    backgroundColor: colors.brand.primary,
    borderColor: colors.brand.primary,
  },
});