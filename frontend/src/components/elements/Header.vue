<template>
  <button 
    @click="toggleMenu" 
    class="cursor-pointer text-2xl fixed top-3 left-6 z-50 transition-all duration-300 ease-in"
  >
    <Bars3Icon v-if="!isMenuOpen" class="h-8 w-8 text-gray-800 dark:text-gray-200" />
  </button>

  
  <div 
    :class="['nav nav-red bg-[#7A1316] w-[50%] max-w-96 fixed top-0 left-0 h-screen transition-all duration-500 ease-in z-40', isMenuOpen ? 'visible' : '']"
  >
    <div 
      :class="['nav nav-sand bg-[#BA9b76] w-[95%] h-screen transition-all duration-500 ease-in', isMenuOpen ? 'visible' : '']"
    >
      <div 
        :class="['nav nav-white bg-[#2a2a2a] w-[95%] px-6 left-0 h-screen transition-all duration-500 ease-in relative p-12', isMenuOpen ? 'visible' : '']"
      >
        <button 
          @click="toggleMenu" 
          class="cursor-pointer text-2xl absolute top-3 left-6 transition-all duration-300 ease-in"
        >
          <XMarkIcon v-if="isMenuOpen" class="h-8 w-8 text-gray-800 dark:text-gray-200" />
        </button>
        
        <img class="h-20 mt-6 mx-0 rounded-full bg-white p-4" :src="logo" alt="Logo">
        
        <ul class="mt-12 ml-1 flex flex-col gap-4 text-lg text-white font-light">
          <li v-for="item in navigation" :key="item.name">
            <router-link :to="item.href" @click="closeMenu">{{ item.name }}</router-link>
            
            <!-- Show categories if this is the Shop item -->
            <ul v-if="item.name === 'Shop' && categories.length > 0" class="ml-5 flex flex-col gap-2 mt-2">
              <li v-for="category in categories" :key="category.id">
                <router-link 
                  :to="`/shop/category/${category.slug}`" 
                  @click="closeMenu"
                >
                  {{ category.name }}
                </router-link>
              </li>
            </ul>
          </li>
        </ul>
      </div>
    </div>
  </div>
</template>

<script setup lang="ts">
import { ref, onMounted } from 'vue'
import { apiCall } from '@/api/client'
import logo from '@/assets/img/eclectica-logo.png'
import { Bars3Icon, XMarkIcon } from '@heroicons/vue/24/outline'

interface Category {
  id: number
  name: string
  slug: string
}

const isMenuOpen = ref(false)
const categories = ref<Category[]>([])

const navigation = [
  { name: 'Home', href: '/' },
  { name: 'About', href: '/about' },
  { name: 'Blog', href: '/blog' },
  { name: 'Shop', href: '/shop' },
  { name: 'Contact', href: '/contact' },
]

const toggleMenu = () => {
  isMenuOpen.value = !isMenuOpen.value
}

const closeMenu = () => {
  isMenuOpen.value = false
}

const fetchCategories = async () => {
  try {
    categories.value = await apiCall<Category[]>('/store/categories/')
  } catch (error) {
    console.error('Failed to fetch categories:', error)
  }
}

onMounted(() => {
  fetchCategories()
})
</script>

<style scoped>
.nav {
  transform: translateX(-100%);
}

.nav.visible {
  transform: translateX(0);
}
</style>