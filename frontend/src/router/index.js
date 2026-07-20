import { createRouter, createWebHistory } from 'vue-router'

const routes = [
  {
    path: '/',
    redirect: '/entry'
  },
  {
    path: '/entry',
    name: 'SalesEntry',
    component: () => import('../views/SalesEntry.vue'),
    meta: { title: '数据录入' }
  },
  {
    path: '/salespersons',
    name: 'Salespersons',
    component: () => import('../views/Salespersons.vue'),
    meta: { title: '业务员管理' }
  },
  {
    path: '/reports',
    name: 'Reports',
    component: () => import('../views/Reports.vue'),
    meta: { title: '报表' }
  }
]

const router = createRouter({
  history: createWebHistory(),
  routes
})

export default router
