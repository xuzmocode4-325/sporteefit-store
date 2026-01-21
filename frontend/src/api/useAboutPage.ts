/**
 * About Page API endpoints
 * 
 * Note: This endpoint is not yet implemented in the backend.
 * Add the corresponding API endpoint in backend when ready.
 */

import { apiCall } from './client'

export interface Stat {
  label: string
  value: string | number
}

export interface AboutPage {
  id: number
  title: string
  slug: string
  intro?: string
  body?: any
  stats?: Stat[]
  // Add other fields as defined in your Wagtail AboutPage model
  [key: string]: any
}

/**
 * Get about page content
 * Note: Backend endpoint needs to be created
 */
export async function getAboutPage(): Promise<AboutPage> {
  return apiCall<AboutPage>('/about/')
}
