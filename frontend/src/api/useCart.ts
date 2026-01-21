/**
 * Cart API endpoints
 * 
 * Handles shopping cart operations: add, update, delete items, apply coupons
 */

import { apiCall, apiPost } from './client'

// ========================================
// Type Definitions
// ========================================

export interface CartResponse {
  cart_qty: number
  product_qty: number
}

export interface CartDeletePayload {
  product_id: number
}

export interface CartUpdatePayload {
  product_id: number
  product_qty: number
}

export interface CouponApplyPayload {
  coupon_code: string
}

export interface CouponApplyResponse {
  success: boolean
}

export interface CartItem {
  product_id: number
  name: string
  qty: number
  price: number
  slug: string
}

export interface CartListResponse {
  items: CartItem[]
  cart_qty: number
  total: number
}

// ========================================
// Cart Endpoints
// ========================================

/**
 * Delete item from cart
 */
export async function deleteFromCart(payload: CartDeletePayload): Promise<CartResponse> {
  return apiPost<CartDeletePayload, CartResponse>('/cart/delete', payload)
}

/**
 * Update cart item quantity
 */
export async function updateCart(payload: CartUpdatePayload): Promise<CartResponse> {
  return apiPost<CartUpdatePayload, CartResponse>('/cart/update', payload)
}

/**
 * Apply coupon code to cart
 */
export async function applyCoupon(payload: CouponApplyPayload): Promise<CouponApplyResponse> {
  return apiPost<CouponApplyPayload, CouponApplyResponse>('/cart/apply-coupon', payload)
}

/**
 * Get all items in cart
 */
export async function getCartItems(): Promise<CartListResponse> {
  return apiCall<CartListResponse>('/cart/items')
}
