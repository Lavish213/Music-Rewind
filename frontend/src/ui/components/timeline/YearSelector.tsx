import React from "react";
import { View, Text, Pressable, StyleSheet } from "react-native";

type Props = {
  years: number[];
  selectedYear: number | null;
  onSelectYear: (year: number | null) => void;
};

export function YearSelector({
  years,
  selectedYear,
  onSelectYear,
}: Props) {
  return (
    <View style={styles.container}>
      {/* All */}
      <Pressable onPress={() => onSelectYear(null)}>
        <Text
          style={[
            styles.year,
            selectedYear === null && styles.selected,
          ]}
        >
          All
        </Text>
      </Pressable>

      {/* Individual years */}
      {years.map((year) => (
        <Pressable key={year} onPress={() => onSelectYear(year)}>
          <Text
            style={[
              styles.year,
              selectedYear === year && styles.selected,
            ]}
          >
            {year}
          </Text>
        </Pressable>
      ))}
    </View>
  );
}

const styles = StyleSheet.create({
  container: {
    flexDirection: "row",
    gap: 12,
    paddingVertical: 12,
  },
  year: {
    fontSize: 16,
    color: "#888",
  },
  selected: {
    fontWeight: "700",
    color: "#000",
  },
});