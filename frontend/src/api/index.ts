// ========================================
// API Client
// ========================================
export { apiCall, apiPost } from './client'
export type { ApiResponse } from './client'

// ========================================
// Accounts & Authentication
// ========================================
export {
  setCsrfToken,
  registerUser,
  verifyEmail,
  loginUser,
  logoutUser,
  getUserProfile,
  updateProfile,
  uploadProfileImage,
  deleteAccount,
  adminCreateUser,
  getUserDetail,
  updateUser,
  deleteUser,
} from './useAccounts'

export type {
  MessageResponse,
  UserRegisterPayload,
  UserLoginPayload,
  UserProfile,
  ProfileUpdatePayload,
  UploadImageResponse,
  AdminCreateUserPayload,
  AdminUserUpdatePayload,
} from './useAccounts'

// ========================================
// Blog
// ========================================
export {
  getBlogPosts,
  getBlogPostBySlug,
  getBlogPostById,
} from './useBlog'

export type {
  Author,
  BlogPostListItem,
  GalleryImage,
  BodyBlock,
  BlogPostDetail,
} from './useBlog'

// ========================================
// Cart
// ========================================
export {
  deleteFromCart,
  updateCart,
  applyCoupon,
  getCartItems,
} from './useCart'

export type {
  CartResponse,
  CartDeletePayload,
  CartUpdatePayload,
  CouponApplyPayload,
  CouponApplyResponse,
  CartItem,
  CartListResponse,
} from './useCart'

// ========================================
// Home Page
// ========================================
export { getHomePage } from './useHome'
export type { HomePage } from './useHome'

// ========================================
// Store & Products
// ========================================
export {
  getCategories,
  getProducts,
  getProduct,
  createProduct,
  updateProduct,
  deleteProduct,
} from './useStore'

export type {
  Category,
  Product,
  ProductCreatePayload,
  ProductUpdatePayload,
} from './useStore'

// ========================================
// Payments & Checkout
// ========================================
export {
  getCheckout,
  completeOrder,
} from './usePayments'

export type {
  ShippingAddress,
  CartItemCheckout,
  CheckoutResponse,
  CompleteOrderPayload,
} from './usePayments'