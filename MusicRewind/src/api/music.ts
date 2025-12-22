import { apiFetch } from './client';

export type RewindSummary = {
  topSongs: string[];
  topArtists: string[];
};

export function fetchRewind(): Promise<RewindSummary> {
  return apiFetch('/rewind');
}