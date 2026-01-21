/**
 * Blog API endpoints
 * 
 * Handles blog post listing and detail views
 */

import { apiCall } from './client'

// ========================================
// Type Definitions
// ========================================

export interface Author {
  id: number
  name: string
  bio?: string
  image?: string | null
}

export interface BlogPostListItem {
  id: number
  title: string
  date: string
  quote: string
  intro: string
  first_image?: string | null
  authors: Author[]
  tags: string[]
  slug: string
}

export interface GalleryImage {
  image: string
  caption?: string | null
}

export interface BodyBlock {
  type: string
  value: string | any
}

export interface BlogPostDetail {
  id: number
  title: string
  slug: string
  date: string
  quote: string
  intro: string
  body: BodyBlock[]
  authors: Author[]
  tags: string[]
  gallery_images: GalleryImage[]
  category?: string | null
}

// ========================================
// Blog Endpoints
// ========================================

/**
 * Get list of all published blog posts
 */
export async function getBlogPosts(): Promise<BlogPostListItem[]> {
  return apiCall<BlogPostListItem[]>('/blog/posts/')
}

/**
 * Get single blog post by slug
 */
export async function getBlogPostBySlug(slug: string): Promise<BlogPostDetail> {
  return apiCall<BlogPostDetail>(`/blog/post/${slug}/`)
}

/**
 * Get single blog post by ID
 */
export async function getBlogPostById(id: number): Promise<BlogPostDetail> {
  return apiCall<BlogPostDetail>(`/blog/post/${id}/`)
}
