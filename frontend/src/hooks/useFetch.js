import { useState, useEffect, useCallback } from "react";
import { useAuth } from "./useAuth";

const API_URL = import.meta.env.VITE_API_URL;

export function useFetch(path, options = {}) {
  const { token } = useAuth();
  const [data, setData] = useState(null);
  const [loading, setLoading] = useState(!options.skip);
  const [error, setError] = useState(null);

  const optionsKey = JSON.stringify(options);

  const fetchData = useCallback(() => {
    if (options.skip || !path) {
      setLoading(false);
      return;
    }

    setLoading(true);
    setError(null);

    const headers = {
      "Content-Type": "application/json",
      ...(token ? { Authorization: `Bearer ${token}` } : {}),
      ...options.headers,
    };

    fetch(`${API_URL}${path}`, { ...options, headers })
      .then(async (res) => {
        const body = await res.json().catch(() => null);
        if (!res.ok) {
          throw new Error(body?.error || `Request failed (${res.status})`);
        }
        return body;
      })
      .then(setData)
      .catch((err) => setError(err.message))
      .finally(() => setLoading(false));
    // eslint-disable-next-line react-hooks/exhaustive-deps
  }, [path, token, optionsKey]);

  useEffect(() => {
    fetchData();
  }, [fetchData]);

  return { data, loading, error, refetch: fetchData };
}