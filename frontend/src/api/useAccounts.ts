/**
 * Account/Auth API endpoints
 * 
 * Handles user authentication, registration, profile management, and admin user operations
 */

import { apiCall, apiPost } from './client'

// ========================================
// Type Definitions
// ========================================

export interface MessageResponse {
  detail: string
}

export interface UserRegisterPayload {
  username: string
  email: string
  password: string
}

export interface UserLoginPayload {
  username?: string
  email?: string
  password: string
}

export interface UserProfile {
  id: number
  username: string
  email: string
  name: string
  surname: string
  is_active: boolean
  is_staff: boolean
}

export interface ProfileUpdatePayload {
  name?: string
  surname?: string
}

export interface UploadImageResponse {
  detail: string
  image: string
}

export interface AdminCreateUserPayload {
  username: string
  email: string
  password: string
  name: string
  surname: string
  is_active: boolean
  is_staff: boolean
}

export interface AdminUserUpdatePayload {
  username?: string
  email?: string
  password?: string
  name?: string
  surname?: string
  is_active?: boolean
  is_staff?: boolean
}

// ========================================
// Authentication Endpoints
// ========================================

/**
 * Set CSRF token cookie for clients
 */
export async function setCsrfToken(): Promise<MessageResponse> {
  return apiCall<MessageResponse>('/accounts/set-csrf-token')
}

/**
 * Register a new user account
 */
export async function registerUser(payload: UserRegisterPayload): Promise<MessageResponse> {
  return apiPost<UserRegisterPayload, MessageResponse>('/accounts/register', payload)
}

/**
 * Verify email with token from verification link
 */
export async function verifyEmail(uidb64: string, token: string): Promise<MessageResponse> {
  return apiCall<MessageResponse>(`/accounts/verify-email/${uidb64}/${token}`)
}

/**
 * Login user with username/email and password
 */
export async function loginUser(payload: UserLoginPayload): Promise<MessageResponse> {
  return apiPost<UserLoginPayload, MessageResponse>('/accounts/login', payload)
}

/**
 * Logout current user
 */
export async function logoutUser(): Promise<MessageResponse> {
  return apiPost<{}, MessageResponse>('/accounts/logout', {})
}

// ========================================
// Profile Management
// ========================================

/**
 * Get current user's profile
 */
export async function getUserProfile(): Promise<UserProfile> {
  return apiCall<UserProfile>('/accounts/profile')
}

/**
 * Update current user's profile
 * Note: This endpoint expects FormData, so we'll need a special handler
 */
export async function updateProfile(data: ProfileUpdatePayload): Promise<any> {
  const formData = new FormData()
  if (data.name !== undefined) formData.append('name', data.name)
  if (data.surname !== undefined) formData.append('surname', data.surname)

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
  const csrfToken = getCsrfToken()
  
  const headers: HeadersInit = {}
  if (csrfToken) {
    headers['X-CSRFToken'] = csrfToken
  }

  const response = await fetch(`${API_BASE_URL}/accounts/profile`, {
    method: 'PATCH',
    headers,
    body: formData,
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return response.json()
}

/**
 * Upload profile image
 */
export async function uploadProfileImage(imageFile: File): Promise<UploadImageResponse> {
  const formData = new FormData()
  formData.append('image', imageFile)

  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
  const csrfToken = getCsrfToken()
  
  const headers: HeadersInit = {}
  if (csrfToken) {
    headers['X-CSRFToken'] = csrfToken
  }

  const response = await fetch(`${API_BASE_URL}/accounts/upload-profile-image`, {
    method: 'POST',
    headers,
    body: formData,
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return response.json()
}

/**
 * Delete current user's account
 */
export async function deleteAccount(): Promise<MessageResponse> {
  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
  const csrfToken = getCsrfToken()
  
  const headers: HeadersInit = {}
  if (csrfToken) {
    headers['X-CSRFToken'] = csrfToken
  }

  const response = await fetch(`${API_BASE_URL}/accounts/profile`, {
    method: 'DELETE',
    headers,
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return response.json()
}

// ========================================
// Admin User Management
// ========================================

/**
 * Admin: Create a new user
 */
export async function adminCreateUser(payload: AdminCreateUserPayload): Promise<UserProfile> {
  return apiPost<AdminCreateUserPayload, UserProfile>('/accounts/users', payload)
}

/**
 * Admin: Get user details by ID
 */
export async function getUserDetail(userId: number): Promise<UserProfile> {
  return apiCall<UserProfile>(`/accounts/users/${userId}`)
}

/**
 * Admin: Update user details
 */
export async function updateUser(userId: number, payload: AdminUserUpdatePayload): Promise<UserProfile> {
  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
  const csrfToken = getCsrfToken()
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  }
  if (csrfToken) {
    headers['X-CSRFToken'] = csrfToken
  }

  const response = await fetch(`${API_BASE_URL}/accounts/users/${userId}`, {
    method: 'PATCH',
    headers,
    body: JSON.stringify(payload),
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return response.json()
}

/**
 * Admin: Delete a user
 */
export async function deleteUser(userId: number): Promise<MessageResponse> {
  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
  const csrfToken = getCsrfToken()
  
  const headers: HeadersInit = {}
  if (csrfToken) {
    headers['X-CSRFToken'] = csrfToken
  }

  const response = await fetch(`${API_BASE_URL}/accounts/users/${userId}`, {
    method: 'DELETE',
    headers,
    credentials: 'include',
  })

  if (!response.ok) {
    throw new Error(`API error: ${response.status}`)
  }

  return response.json()
}

// ========================================
// Helper Functions
// ========================================

function getCsrfToken(): string | null {
  const name = 'csrftoken'
  let cookieValue: string | null = null
  if (document.cookie && document.cookie !== '') {
    const cookies = document.cookie.split(';')
    for (let i = 0; i < cookies.length; i++) {
      const raw = cookies[i]
      if (!raw) continue
      const cookie = raw.trim()
      if (cookie.substring(0, name.length + 1) === (name + '=')) {
        cookieValue = decodeURIComponent(cookie.substring(name.length + 1))
        break
      }
    }
  }
  return cookieValue
}
