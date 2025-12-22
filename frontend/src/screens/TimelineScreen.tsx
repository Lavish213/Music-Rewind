import React, { useEffect, useMemo, useState } from "react";
import {
  ScrollView,
  StyleSheet,
  View,
  ActivityIndicator,
  Text,
} from "react-native";

import Animated, { FadeInUp, Layout } from "react-native-reanimated";

import { TimelineHeader } from "../ui/components/timeline/TimelineHeader";
import { YearSelector } from "../ui/components/timeline/YearSelector";
import { SongMemoryCard } from "../ui/components/timeline/SongMemoryCard";
import { colors, spacing } from "../ui/tokens";
import { API_BASE_URL } from "../config/api";

/**
 * DO NOT CHANGE:
 * Animation wrapper for each card.
 * Cards themselves remain untouched.
 */
function AnimatedTimelineItem({
  children,
  index,
}: {
  children: React.ReactNode;
  index: number;
}) {
  return (
    <Animated.View
      entering={FadeInUp.delay(index * 80)}
      layout={Layout.springify()}
      style={styles.cardWrapper}
    >
      {children}
    </Animated.View>
  );
}

/* ----------------------------- Types ----------------------------- */

type TimelineItem = {
  id: string;
  title: string;
  artist: string;
  year: number;
  note?: string;
};

/* -------------------------- Screen -------------------------- */

export function TimelineScreen() {
  const [items, setItems] = useState<TimelineItem[]>([]);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState<string | null>(null);
  const [selectedYear, setSelectedYear] = useState<number | null>(null);
  const [hasTimeline, setHasTimeline] = useState<boolean | null>(null);

  /* -------- Fetch timeline data -------- */

  useEffect(() => {
    fetch(`${API_BASE_URL}/api/v1/timeline`)
      .then((res) => res.json())
      .then((data) => {
        const timelineItems = data.items ?? [];
        setItems(timelineItems);
        setHasTimeline(timelineItems.length > 0);
        setError(null);
      })
      .catch(() => {
        setItems([]);
        setHasTimeline(false);
        setError("Could not load timeline");
      })
      .finally(() => setLoading(false));
  }, []);

  /* -------- Derived data -------- */

  const years = useMemo(
    () =>
      Array.from(new Set(items.map((i) => i.year))).sort((a, b) => b - a),
    [items]
  );

  const filtered = useMemo(() => {
    if (selectedYear == null) return items;
    return items.filter((i) => i.year === selectedYear);
  }, [items, selectedYear]);

  /* -------------------------- Render -------------------------- */

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      showsVerticalScrollIndicator={false}
    >
      <TimelineHeader />

      <YearSelector
        years={years}
        selectedYear={selectedYear}
        onSelectYear={setSelectedYear}
      />

      {/* Loading */}
      {loading && (
        <View style={styles.center}>
          <ActivityIndicator color={colors.brand.primary} />
        </View>
      )}

      {/* Error */}
      {error && (
        <View style={styles.center}>
          <SongMemoryCard title="Error" artist="" year={0} note={error} />
        </View>
      )}

      {/* Empty timeline */}
      {!loading && !error && filtered.length === 0 && (
        <View style={styles.center}>
          <SongMemoryCard
            title="No memories yet"
            artist=""
            year={0}
            note="Add your first song memory to start your timeline."
          />
        </View>
      )}

      {/* Helper text */}
      {hasTimeline === false && (
        <Text style={styles.helperText}>
          Your timeline is empty. Add a memory to get started.
        </Text>
      )}

      {/* Timeline list */}
      {!loading && !error && filtered.length > 0 && (
        <View style={styles.list}>
          {filtered.map((item, index) => (
            <AnimatedTimelineItem
              key={item.id ?? `${item.year}-${index}`}
              index={index}
            >
              <SongMemoryCard
                title={item.title}
                artist={item.artist}
                year={item.year}
                note={item.note ?? ""}
              />
            </AnimatedTimelineItem>
          ))}
        </View>
      )}
    </ScrollView>
  );
}

/* -------------------------- Styles -------------------------- */

const styles = StyleSheet.create({
  container: {
    flex: 1,
    backgroundColor: colors.background.app,
  },
  content: {
    paddingTop: spacing.md,
    paddingBottom: spacing.xl,
  },
  list: {
    paddingHorizontal: spacing.md,
  },
  cardWrapper: {
    marginBottom: spacing.md,
  },
  center: {
    paddingVertical: spacing.lg,
    alignItems: "center",
  },
  helperText: {
    marginTop: spacing.sm,
    color: colors.text.secondary,
    fontSize: 14,
    textAlign: "center",
  },
});