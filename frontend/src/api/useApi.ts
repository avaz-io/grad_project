import { useEffect, useState } from "react";

type ApiState<T> = {
  data: T | null;
  loading: boolean;
  error: boolean;
  retry: () => void;
};

// Runs `load` when the page opens, and again whenever a value in `deps` changes
// (for example a filter). Keeps track of the loading and error states for the page.
export function useApi<T>(load: () => Promise<T>, deps: unknown[] = []): ApiState<T> {
  const [data, setData] = useState<T | null>(null);
  const [loading, setLoading] = useState(true);
  const [error, setError] = useState(false);
  const [attempt, setAttempt] = useState(0); // retry() increases it to load again

  useEffect(() => {
    // If a filter changes before the old request finishes,
    // the old answer must not overwrite the new one.
    let ignore = false;
    setLoading(true);
    setError(false);

    load()
      .then((result) => {
        if (!ignore) setData(result);
      })
      .catch(() => {
        if (!ignore) setError(true);
      })
      .finally(() => {
        if (!ignore) setLoading(false);
      });

    return () => {
      ignore = true;
    };
    // `load` is a new function on every render, so it is left out on purpose;
    // the page lists the values `load` depends on in `deps` instead.
  }, [...deps, attempt]);

  return { data, loading, error, retry: () => setAttempt((n) => n + 1) };
}
