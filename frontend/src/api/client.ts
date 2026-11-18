// Base URL of the backend API. Set VITE_API_URL in a .env file to change it.
const API_URL = import.meta.env.VITE_API_URL ?? "http://localhost:8000/api/v1";

export async function getHealth(): Promise<{ status: string }> {
  const response = await fetch(`${API_URL}/health/`);
  if (!response.ok) {
    throw new Error(`API error: ${response.status}`);
  }
  return response.json();
}
