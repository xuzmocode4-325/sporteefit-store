import { createRouter, createWebHistory } from 'vue-router'
import HomePage from '@/components/HomePage.vue'
import AboutPage from '@/components/AboutPage.vue'
import BlogPage from '@/components/BlogPage.vue'
import ContactPage from '@/components/ContactPage.vue'
import BlogPostView from '@/components/BlogPostView.vue'
import BlogPreviewView from '@/components/BlogPreviewView.vue'
import TagIndexView from '@/components/TagIndexView.vue'
import ShopHomePage from '@/components/ShopHomePage.vue'

const routes = [
  // Expected Vue routes
  { path: '/', component: HomePage }, // Home page
  { path: '/about/', component: AboutPage }, // About page
  { path: '/blog/', component: BlogPage }, // Blog listing page
  { path: '/blog/:slug', component: BlogPostView }, // BlogPostPage live (preview uses /blog/preview/)
  { path: '/blog/preview/', component: BlogPreviewView }, // Handles token
  { path: '/tags/', component: TagIndexView },
  { path: '/contact/', component: ContactPage }, // Contact page
  { path: '/shop/', component: ShopHomePage }, // Shop home page
]

const router = createRouter({
  history: createWebHistory(import.meta.env.BASE_URL),
  routes: routes,
})

export default router
