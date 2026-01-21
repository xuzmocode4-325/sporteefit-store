<template>
  <div class="relative bg-[#2a2a2a] min-h-screen overflow-hidden">
    <div class="mx-auto max-w-7xl lg:grid lg:grid-cols-12 lg:gap-x-8 lg:px-8">
      <div class="px-6 pt-10 pb-24 sm:pb-32 lg:col-span-7 lg:px-0 lg:pt-40 lg:pb-48 xl:col-span-6">
        <div class="mx-auto max-w-lg lg:mx-0">
          <img class="h-20 bg-white rounded-full p-4" :src="logo" alt="Your Company" />
          <div class="hidden sm:mt-32 sm:flex lg:mt-16">
            <div class="relative rounded-full px-3 py-1 text-sm/6 text-gray-300 ring-1 ring-white/10 hover:ring-white/20">
              Discover contemporary art that captivates & collects value &nbsp;
              <a href="/blog" class="font-semibold whitespace-nowrap text-[#BA9b76]">
                <span class="absolute inset-0" aria-hidden="true">
                </span>Read more <span aria-hidden="true">&rarr;</span>
              </a>
            </div>
          </div>
          <h1 class="mt-24 text-5xl font-semibold tracking-tight text-pretty text-gray-900 sm:mt-10 sm:text-7xl dark:text-white">
            The home of everything classical art and antiques
          </h1>
          <p class="mt-8 text-lg font-medium text-pretty text-gray-300 sm:text-xl/8">
            Eclectica Contemporary curates exclusive modern masterpieces from South Africa's boldest artists. Transform your space with art that demands attention and appreciates over time. Start collecting today.
          </p>
          <div class="mt-10 flex items-center gap-x-6">
            <a href="/shop" class="rounded-md bg-[#7A1316] px-3.5 py-2.5 text-sm font-semibold text-white shadow-xs hover:bg-[#9B1B1E] focus-visible:outline-2 focus-visible:outline-offset-2 focus-visible:outline-[#9B1B1E] dark:bg-[#9B1B1E] dark:hover:bg-[#7A1316] dark:focus-visible:outline-[#7A1316]">
              Shop now
            </a>
            <a href="#" class="text-sm/6 font-semibold text-gray-900 dark:text-white">
              Learn more 
              <span aria-hidden="true">→</span>
            </a>
          </div>
        </div>
      </div>
      <div class="relative lg:col-span-5 lg:-mr-8 xl:absolute xl:inset-0 xl:left-1/2 xl:mr-0">
        <img class="aspect-3/2 w-full bg-gray-50 object-cover lg:absolute lg:inset-0 lg:aspect-auto lg:h-full dark:bg-gray-800" :src="featuredImage" alt="Featured Art" />
      </div>
    </div>
  </div>
</template>
<script setup>
  import logo from '@/assets/img/eclectica-logo.png'
  import featuredImage from '@/assets/img/featured-art.jpg'
</script>