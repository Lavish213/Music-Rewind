export type RewindSummary = {
  user: {
    name: string;
  };
  topArtist: string;
  topSong: string;
  minutesPlayed: number;
};

const API_BASE = process.env.EXPO_PUBLIC_API_URL;

export async function fetchRewindSummary(): Promise<RewindSummary> {
  if (!API_BASE) {
    throw new Error('API base URL not configured');
  }

  const res = await fetch(`${API_BASE}/api/v1/rewind/summary`);

  if (!res.ok) {
    throw new Error('Failed to load rewind data');
  }

  return res.json();
}