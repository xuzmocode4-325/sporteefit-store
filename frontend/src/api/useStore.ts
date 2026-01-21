/**
 * Store/Products API endpoints
 * 
 * Handles product and category management
 */

import { apiCall, apiPost } from './client'

// ========================================
// Type Definitions
// ========================================

export interface MessageResponse {
  detail: string
}

export interface Category {
  id: number
  name: string
  slug: string
  // Add other category fields as needed
}

export interface Product {
  id: number
  name: string
  brand?: string
  description?: string
  slug: string
  price: number
  discount?: number
  category?: Category | null
  // Add other product fields as needed
}

export interface ProductCreatePayload {
  name: string
  brand?: string
  description?: string
  slug: string
  price: number
  discount?: number
  category_id?: number | null
}

export interface ProductUpdatePayload {
  name?: string
  brand?: string
  description?: string
  slug?: string
  price?: number
  discount?: number
  category?: number
  tags?: number[]
}

// ========================================
// Category Endpoints
// ========================================

/**
 * Get all categories
 */
export async function getCategories(): Promise<Category[]> {
  return apiCall<Category[]>('/store/categories/')
}

// ========================================
// Product Endpoints
// ========================================

/**
 * Get all products
 */
export async function getProducts(): Promise<Product[]> {
  return apiCall<Product[]>('/store/products/')
}

/**
 * Get single product by ID
 */
export async function getProduct(productId: number): Promise<Product> {
  return apiCall<Product>(`/store/products/${productId}`)
}

/**
 * Create new product (requires staff authentication)
 */
export async function createProduct(payload: ProductCreatePayload): Promise<Product> {
  return apiPost<ProductCreatePayload, Product>('/store/products/', payload)
}

/**
 * Update existing product (requires staff authentication)
 */
export async function updateProduct(productId: number, payload: ProductUpdatePayload): Promise<Product> {
  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
  const csrfToken = getCsrfToken()
  
  const headers: HeadersInit = {
    'Content-Type': 'application/json',
  }
  if (csrfToken) {
    headers['X-CSRFToken'] = csrfToken
  }

  const response = await fetch(`${API_BASE_URL}/store/products/${productId}`, {
    method: 'PUT',
    headers,
    body: JSON.stringify(payload),
    credentials: 'include',
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `API error: ${response.status}`)
  }

  return response.json()
}

/**
 * Delete product (requires staff authentication)
 */
export async function deleteProduct(productId: number): Promise<MessageResponse> {
  const API_BASE_URL = import.meta.env.VITE_API_URL || 'http://localhost:8000/api'
  const csrfToken = getCsrfToken()
  
  const headers: HeadersInit = {}
  if (csrfToken) {
    headers['X-CSRFToken'] = csrfToken
  }

  const response = await fetch(`${API_BASE_URL}/store/products/${productId}`, {
    method: 'DELETE',
    headers,
    credentials: 'include',
  })

  if (!response.ok) {
    const errorData = await response.json().catch(() => ({}))
    throw new Error(errorData.detail || `API error: ${response.status}`)
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
