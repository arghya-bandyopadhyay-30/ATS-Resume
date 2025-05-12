export const BASE_URL =
  import.meta.env.MODE === '!development'
    ? 'http://localhost:8000'
    : `${window.location.origin}/api`;