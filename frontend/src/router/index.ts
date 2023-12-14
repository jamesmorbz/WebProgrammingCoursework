import { createRouter, createWebHistory } from 'vue-router'

import MainPage from '@/pages/MainPage.vue'
import OtherPage from '@/pages/OtherPage.vue'
import ProfilePage from '@/pages/ProfilePage.vue'
import ArticlePage from '@/pages/ArticlePage.vue'
import NewArticlePage from '@/pages/NewArticlePage.vue'
import EditArticlePage from '@/pages/EditArticlePage.vue'

let base = import.meta.env.MODE == 'development' ? import.meta.env.BASE_URL : ''

const router = createRouter({
  history: createWebHistory(base),
  routes: [
    { path: '/', name: 'MainPage', component: MainPage },
    { path: '/other', name: 'OtherPage', component: OtherPage },
    { path: '/profile', name: 'ProfilePage', component: ProfilePage },
    { path: '/article', name: 'NewArticle', component: NewArticlePage },
    {
      path: '/article/:id/edit',
      name: 'EditArticle',
      component: EditArticlePage,
    },
    {
      path: '/article/:id',
      name: 'Article',
      component: ArticlePage,
      props: (route) => ({ id: Number(route.params.id) }),
    },
  ],
})
// Starting to look at using pinia
// router.beforeEach((to) => {
//   const store = useStore()

//   if (to.meta.requiresAuth && !store.isLoggedIn) return '/login'
// })

export default router
