import React, { useEffect, useMemo, useState } from "react";
import {
  ScrollView,
  StyleSheet,
  View,
  ActivityIndicator,
  Pressable,
  Text,
} from "react-native";

import { router } from "expo-router";
import { colors, spacing } from "../../tokens";
import { SongMemoryCard } from "./SongMemoryCard";
import { TimelineHeader } from "./TimelineHeader";
import { DASHBOARD_COPY } from "../../copy/dashboard";
import { API_BASE_URL } from "../../../config/api";

/* ----------------------------- Types ----------------------------- */

type TimelineItem = {
  id: string;
  title: string;
  artist: string;
  year: number;
  note?: string;
};

/* -------------------------- Screen -------------------------- */

export default function DashboardScreen() {
  const [items, setItems] = useState<TimelineItem[]>([]);
  const [loading, setLoading] = useState(true);

  /* -------- Fetch timeline summary -------- */

  useEffect(() => {
    let mounted = true;

    fetch(`${API_BASE_URL}/api/v1/timeline`)
      .then((res) => res.json())
      .then((data) => {
        if (!mounted) return;
        setItems(Array.isArray(data?.items) ? data.items : []);
      })
      .catch(() => {
        if (mounted) setItems([]);
      })
      .finally(() => {
        if (mounted) setLoading(false);
      });

    return () => {
      mounted = false;
    };
  }, []);

  /* -------- Derived stats -------- */

  const stats = useMemo(() => {
    if (items.length === 0) {
      return { total: 0, years: 0, latest: null as TimelineItem | null };
    }

    const years = new Set(items.map((i) => i.year));
    const latest = [...items].sort((a, b) => b.year - a.year)[0];

    return {
      total: items.length,
      years: years.size,
      latest,
    };
  }, [items]);

  /* -------------------------- Render -------------------------- */

  return (
    <ScrollView
      style={styles.container}
      contentContainerStyle={styles.content}
      showsVerticalScrollIndicator={false}
    >
      <TimelineHeader />

      {loading && (
        <View style={styles.center}>
          <ActivityIndicator color={colors.brand.primary} />
        </View>
      )}

      {!loading && items.length === 0 && (
        <View style={styles.center}>
          <SongMemoryCard
            title={DASHBOARD_COPY.empty.title}
            artist=""
            year={0}
            note={DASHBOARD_COPY.empty.body}
          />

          <Pressable
            style={styles.primaryButton}
            onPress={() => router.push("/quick-add")}
          >
            <Text style={styles.primaryButtonText}>
              {DASHBOARD_COPY.empty.cta}
            </Text>
          </Pressable>
        </View>
      )}

      {!loading && items.length > 0 && (
        <>
          <View style={styles.section}>
            <SongMemoryCard
              title={DASHBOARD_COPY.stats.title}
              artist=""
              year={stats.total}
              note={`${stats.years} different years`}
            />
          </View>

          {stats.latest && (
            <View style={styles.section}>
              <SongMemoryCard
                title={stats.latest.title}
                artist={stats.latest.artist}
                year={stats.latest.year}
                note={stats.latest.note ?? ""}
              />
            </View>
          )}

          <View style={styles.actions}>
            <Pressable
              style={styles.primaryButton}
              onPress={() => router.push("/timeline")}
            >
              <Text style={styles.primaryButtonText}>
                {DASHBOARD_COPY.actions.timeline}
              </Text>
            </Pressable>

            <Pressable
              style={styles.secondaryButton}
              onPress={() => router.push("/quick-add")}
            >
              <Text style={styles.secondaryButtonText}>
                {DASHBOARD_COPY.actions.add}
              </Text>
            </Pressable>
          </View>
        </>
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
  center: {
    padding: spacing.lg,
    alignItems: "center",
  },
  section: {
    paddingHorizontal: spacing.md,
    marginBottom: spacing.md,
  },
  actions: {
    marginTop: spacing.lg,
    paddingHorizontal: spacing.md,
    gap: spacing.md,
  },
  primaryButton: {
    backgroundColor: colors.brand.primary,
    paddingVertical: spacing.md,
    borderRadius: 12,
    alignItems: "center",
  },
  primaryButtonText: {
    color: colors.text.primary,
    fontSize: 16,
    fontWeight: "600",
  },
  secondaryButton: {
    borderWidth: 1,
    borderColor: colors.border.light,
    paddingVertical: spacing.md,
    borderRadius: 12,
    alignItems: "center",
  },
  secondaryButtonText: {
    color: colors.text.primary,
    fontSize: 16,
    fontWeight: "500",
  },
});