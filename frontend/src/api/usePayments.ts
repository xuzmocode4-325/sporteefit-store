/**
 * Payments API endpoints
 * 
 * Handles checkout process and order completion
 */

import { apiCall, apiPost } from './client'

// ========================================
// Type Definitions
// ========================================

export interface MessageResponse {
  detail: string
}

export interface ShippingAddress {
  user_id: number
  address1: string
  address2?: string
  city: string
  state?: string
  country: string
  zipcode: string
}

export interface CartItemCheckout {
  product: any
  qty: number
  price: number
  slug: string
}

export interface CheckoutResponse {
  countries: [string, string][] // Array of [code, name] tuples
  cart: CartItemCheckout[]
  shipping: ShippingAddress | null
}

export interface CompleteOrderPayload {
  fn: string // First name
  sn: string // Surname/Last name
  em: string // Email
  ad1: string // Address line 1
  ad2?: string // Address line 2
  ct: string // City
  st?: string // State
  cntry: string // Country
  zip: string // Zipcode
}

// ========================================
// Payment Endpoints
// ========================================

/**
 * Get checkout information including countries, cart items, and shipping address
 */
export async function getCheckout(): Promise<CheckoutResponse> {
  return apiCall<CheckoutResponse>('/payments/checkout')
}

/**
 * Complete order with shipping and payment information
 */
export async function completeOrder(payload: CompleteOrderPayload): Promise<MessageResponse> {
  return apiPost<CompleteOrderPayload, MessageResponse>('/payments/complete-order', payload)
}
