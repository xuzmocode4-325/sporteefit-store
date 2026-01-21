/**
 * API Client for the Django backend.
 *
 * - `API_BASE_URL` is resolved from the Vite env var `VITE_API_URL` or falls
 *   back to a sensible localhost address for development.
 */

const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'

/**
 * Retrieve CSRF token from the browser cookies.
 * Django conventionally stores the CSRF token in a `csrftoken` cookie.
 * Returns the token string when present or `null` when not found.
 */
function getCsrfToken(): string | null {
  const name = 'csrftoken'
  let cookieValue: string | null = null
  if (document.cookie && document.cookie !== '') {
    // Split all cookies and search for the one named 'csrftoken'
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const raw = cookies[i]
      if (!raw) continue
      const cookie = raw.trim()
      // cookie looks like 'csrftoken=VALUE' so check prefix
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}

/**
 * Generic API response shape used by consumers (not required by functions
 * below but useful across the app).
 */
export interface ApiResponse<T> {
  data: T | null
  error: string | null
  loading: boolean
}

/**
 * Perform a GET request to the API and parse JSON.
 *
 * - `endpoint` should begin with a leading slash, e.g. `/products/`.
 * - Throws an Error on HTTP or network failure so callers can handle it.
 */
export async function apiCall<T>(endpoint: string): Promise<T> {
  const url = `${API_BASE_URL}${endpoint}`

  try {
    const response = await fetch(url, {
      method: 'GET',
      headers: {
        'Content-Type': 'application/json',
      },
    })

    // Non-2xx responses are treated as errors and surface a helpful message
    if (!response.ok) {
      throw new Error(`API error: ${response.status} ${response.statusText}`)
    }

    return (await response.json()) as T
  } catch (err) {
    throw new Error(`Failed to fetch ${endpoint}: ${err instanceof Error ? err.message : String(err)}`)
  }
}

/**
 * Perform a POST request to the API with JSON body.
 *
 * - Automatically includes a CSRF token (when present) in the `X-CSRFToken`
 *   header and sends cookies via `credentials: 'include'` so Django can
 *   validate the request.
 * - `T` is the request body type, `U` is the expected response type.
 */
export async function apiPost<T, U>(endpoint: string, body: T): Promise<U> {
  const url = `${API_BASE_URL}${endpoint}`
  const csrfToken = getCsrfToken()

  try {
    const headers: HeadersInit = {
      'Content-Type': 'application/json',
    }
    
    // Attach CSRF token when available (Django expects this for non-safe methods)
    if (csrfToken) {
      headers['X-CSRFToken'] = csrfToken
    }

    const response = await fetch(url, {
      method: 'POST',
      headers,
      body: JSON.stringify(body),
      credentials: 'include', // Ensure cookies are sent for CSRF verification
    })

    if (!response.ok) {
      // Try to extract a helpful error message from the response body if present
      const errorData = await response.json().catch(() => ({}))
      throw new Error(errorData.message || `API error: ${response.status} ${response.statusText}`)
    }

    return (await response.json()) as U
  } catch (err) {
    throw new Error(`Failed to post to ${endpoint}: ${err instanceof Error ? err.message : String(err)}`)
  }
}
