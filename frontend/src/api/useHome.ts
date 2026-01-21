/**
 * Home API endpoints
 * 
 * Fetches home page content from Wagtail CMS
 */

import { apiCall } from './client'

// ========================================
// Type Definitions
// ========================================

export interface HomePage {
  id: number
  title: string
  slug: string
  // Add other fields as defined in your HomePageSchema
  // This will depend on your Wagtail HomePage model structure
  [key: string]: any
}

// ========================================
// Home Page Endpoints
// ========================================

/**
 * Get home page content
 */
export async function getHomePage(): Promise<HomePage> {
  return apiCall<HomePage>('/home/')
}
