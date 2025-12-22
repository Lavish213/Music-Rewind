const API_BASE = "http://127.0.0.1:8000/api/v1";

export async function fetchTimeline(year?: number) {
  const url = year
    ? `${API_BASE}/timeline?year=${year}`
    : `${API_BASE}/timeline`;

  const res = await fetch(url);
  if (!res.ok) throw new Error("Failed to load timeline");

  return res.json();
}