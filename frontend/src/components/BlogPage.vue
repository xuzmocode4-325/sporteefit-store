<template>
  <div class="py-24 sm:py-32 bg-[#2a2a2a] min-h-screen">
    <div class="mx-auto max-w-7xl px-6 lg:px-8">
      <div class="mx-auto max-w-2xl lg:max-w-4xl">
        <img class="h-20 bg-white rounded-full p-4" :src="logo" alt="Your Company" />
        <h2 class="text-4xl mt-12 font-semibold tracking-tight text-pretty text-white">From the blog</h2>
        <p class="mt-2 text-lg/8 text-gray-400">Antique Art Insights, Stories & Collecting Tips.</p>
        <div class="mt-16 space-y-20 lg:mt-20">
          <article v-for="post in posts" :key="post.id" class="relative isolate flex flex-col gap-8 lg:flex-row">
            <div class="relative aspect-video sm:aspect-2/1 lg:aspect-square lg:w-64 lg:shrink-0">
              <img :src="post.imageUrl" alt="" class="absolute inset-0 size-full rounded-2xl bg-gray-50 object-cover dark:bg-gray-800" />
              <div class="absolute inset-0 rounded-2xl inset-ring inset-ring-gray-900/10 dark:inset-ring-white/10"></div>
            </div>
            <div>
              <div class="flex items-center gap-x-4 text-xs">
                <time :datetime="post.datetime" class="text-gray-500 dark:text-gray-400">{{ post.date }}</time>
                <a :href="post.category.href" class="relative z-10 rounded-full px-3 py-1.5 font-medium text-gray-900 bg-[#BA9b76] hover:bg-[#7A1316]">{{ post.category.title }}</a>
              </div>
              <div class="group relative max-w-xl">
                <h3 class="mt-3 text-lg/6 font-semibold text-gray-900 group-hover:text-gray-600 dark:text-white dark:group-hover:text-gray-300">
                  <a :href="post.href">
                    <span class="absolute inset-0"></span>
                    {{ post.title }}
                  </a>
                </h3>
                <p class="mt-5 text-sm/6 text-gray-600 dark:text-gray-400">{{ post.description }}</p>
              </div>
              <div class="mt-6 flex border-t border-gray-900/5 pt-6 dark:border-white/10">
                <div class="relative flex items-center gap-x-4">
                  <img :src="post.author.imageUrl" alt="" class="size-10 rounded-full bg-gray-50 dark:bg-gray-800" />
                  <div class="text-sm/6">
                    <p class="font-semibold text-gray-900 dark:text-white">
                      <a :href="post.author.href">
                        <span class="absolute inset-0"></span>
                        {{ post.author.name }}
                      </a>
                    </p>
                    <p class="text-gray-600 dark:text-gray-400">{{ post.author.role }}</p>
                  </div>
                </div>
              </div>
            </div>
          </article>
        </div>
      </div>
    </div>
  </div>
</template>

<script setup>

  import logo from '@/assets/img/eclectica-logo.png'
const posts = [
  {
    id: 1,
    title: 'Boost your conversion rate',
    href: '#',
    description:
      'Illo sint voluptas. Error voluptates culpa eligendi. Hic vel totam vitae illo. Non aliquid explicabo necessitatibus unde. Sed exercitationem placeat consectetur nulla deserunt vel iusto corrupti dicta laboris incididunt.',
    imageUrl:
      'https://images.unsplash.com/photo-1496128858413-b36217c2ce36?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=3603&q=80',
    date: 'Mar 16, 2020',
    datetime: '2020-03-16',
    category: { title: 'Marketing', href: '#' },
    author: {
      name: 'Michael Foster',
      role: 'Co-Founder / CTO',
      href: '#',
      imageUrl:
        'https://images.unsplash.com/photo-1519244703995-f4e0f30006d5?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    },
  },
  {
    id: 2,
    title: 'How to use search engine optimization to drive sales',
    href: '#',
    description:
      'Optio sit exercitation et ex ullamco aliquid explicabo. Dolore do ut officia anim non ad eu. Magna laboris incididunt commodo elit ipsum.',
    imageUrl:
      'https://images.unsplash.com/photo-1547586696-ea22b4d4235d?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=3270&q=80',
    date: 'Mar 10, 2020',
    datetime: '2020-03-10',
    category: { title: 'Sales', href: '#' },
    author: {
      name: 'Lindsay Walton',
      role: 'Front-end Developer',
      href: '#',
      imageUrl:
        'https://images.unsplash.com/photo-1517841905240-472988babdf9?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    },
  },
  {
    id: 3,
    title: 'Improve your customer experience',
    href: '#',
    description:
      'Dolore commodo in nulla do nulla esse consectetur. Adipisicing voluptate velit sint adipisicing ex duis elit deserunt sint ipsum. Culpa in exercitation magna adipisicing id reprehenderit consectetur culpa eu cillum.',
    imageUrl:
      'https://images.unsplash.com/photo-1492724441997-5dc865305da7?ixlib=rb-4.0.3&ixid=MnwxMjA3fDB8MHxwaG90by1wYWdlfHx8fGVufDB8fHx8&auto=format&fit=crop&w=3270&q=80',
    date: 'Feb 12, 2020',
    datetime: '2020-02-12',
    category: { title: 'Business', href: '#' },
    author: {
      name: 'Tom Cook',
      role: 'Director of Product',
      href: '#',
      imageUrl:
        'https://images.unsplash.com/photo-1472099645785-5658abf4ff4e?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=facearea&facepad=2&w=256&h=256&q=80',
    },
  },
]
</script>