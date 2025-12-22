// frontend/src/ui/copy/dashboard.ts

export const DASHBOARD_COPY = {
  /* ---------------- Header ---------------- */
  header: {
    title: "Your Music Timeline",
    subtitle: "Songs tied to real moments in your life.",
  },

  /* ---------------- Stats ---------------- */
  stats: {
    title: "Memories Saved",
    subtitle: "Across multiple years of your life",
  },

  /* ---------------- Recent ---------------- */
  recent: {
    title: "Most Recent Memory",
    emptyNote: "No note added for this memory.",
  },

  /* ---------------- Actions ---------------- */
  actions: {
    // Buttons used directly in DashboardScreen
    timeline: "Open Timeline",
    add: "Quick Add",

    // Extended labels (not required now, but RESERVED)
    viewTimelineTitle: "View full timeline",
    viewTimelineSubtitle: "Browse your memories year by year",

    addMemoryTitle: "Add a new memory",
    addMemorySubtitle: "Capture a song tied to a moment",
  },

  /* ---------------- Empty State ---------------- */
  empty: {
    title: "Your timeline is empty",
    body:
      "Add a song that reminds you of a moment — we’ll organize it by year.",
    cta: "Add your first memory",
  },

  /* ---------------- Loading ---------------- */
  loading: {
    text: "Loading your memories…",
  },

  /* ---------------- Error ---------------- */
  error: {
    title: "Couldn’t load your timeline",
    body: "Please check your connection and try again.",
  },
} as const;

/* -----------------------------------------
   Strongly-typed export (optional but safe)
------------------------------------------ */
export type DashboardCopy = typeof DASHBOARD_COPY;