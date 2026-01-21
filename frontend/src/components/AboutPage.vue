<template>
  <div class="relative isolate overflow-hidden py-24 sm:py-32 bg-[#2a2a2a] min-h-screen">
    <!-- <div class="hidden sm:absolute sm:-top-10 sm:right-1/2 sm:-z-10 sm:mr-10 sm:block sm:transform-gpu sm:blur-3xl" aria-hidden="true">
      <div class="aspect-1097/845 w-274.25 bg-linear-to-tr from-[#BA9b76] to-[#7A1316] opacity-15 dark:opacity-20" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)"></div>
    </div>
    <div class="absolute -top-52 left-1/2 -z-10 -translate-x-1/2 transform-gpu blur-3xl sm:-top-112 sm:ml-16 sm:translate-x-0" aria-hidden="true">
      <div class="aspect-1097/845 w-274.25 bg-linear-to-tr from-[#BA9b76] to-[#7A1316] opacity-15 dark:opacity-20" style="clip-path: polygon(74.1% 44.1%, 100% 61.6%, 97.5% 26.9%, 85.5% 0.1%, 80.7% 2%, 72.5% 32.5%, 60.2% 62.4%, 52.4% 68.1%, 47.5% 58.3%, 45.2% 34.5%, 27.5% 76.7%, 0.1% 64.9%, 17.9% 100%, 27.6% 76.8%, 76.1% 97.7%, 74.1% 44.1%)"></div>
    </div> -->
    
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
      <img class="h-20 bg-white rounded-full p-4" :src="logo" alt="Your Company" />
      <div class="mt-12 mx-auto max-w-2xl lg:mx-0">
        <h2 class="text-5xl font-semibold tracking-tight sm:text-7xl text-white">Collect with us</h2>
        <p class="mt-8 text-lg font-medium text-pretty sm:text-xl/8 text-gray-300">
          Nestled in the heart of Wynberg, Cape Town, Eclectica Art & Antiques has been curating the finest collection of fine art, sculptures, glassware, porcelain, and antique furniture for over a decade. Our passion for discovery drives us to source one-of-a-kind pieces from around the world, each with its own rich heritage. Whether you're a seasoned collector or furnishing your first dream home, our expert team guides you to masterpieces that elevate everyday living into extraordinary experiences.
        </p>
      </div>
      <div class="mx-auto mt-10 max-w-2xl lg:mx-0 lg:max-w-none">
        <div class="grid grid-cols-1 gap-x-8 gap-y-6 text-base/7 font-semibold text-gray-900 sm:grid-cols-2 md:flex lg:gap-x-10 dark:text-white">
          <a v-for="link in links" :key="link.name" :href="link.href">{{ link.name }} <span aria-hidden="true">&rarr;</span></a>
        </div>
        <dl class="mt-16 grid grid-cols-1 gap-8 sm:mt-20 sm:grid-cols-2 lg:grid-cols-4">
          <div v-for="stat in stats" :key="stat.name" class="flex flex-col-reverse gap-1">
            <dt class="text-base/7 text-gray-700 dark:text-gray-300">{{ stat.name }}</dt>
            <dd class="text-4xl font-semibold tracking-tight text-gray-900 dark:text-white">{{ stat.value }}</dd>
          </div>
        </dl>
      </div>
    </div>
  </div>
</template>

<script setup>
  import logo from '@/assets/img/eclectica-logo.png'
const links = [
  { name: 'Shop now', href: '/shop' },
  // { name: 'Internship program', href: '#' },
  // { name: 'Our values', href: '#' },
  // { name: 'Meet our leadership', href: '#' },
]
const stats = [
  { name: 'Masterpieces Sold', value: '500+' },
  { name: 'Years of excellence', value: '15' },
  { name: 'Client satisfaction', value: '98%' },
  { name: 'Collection value', value: 'R50M+' },
]
</script>