/*
 * Authors: see git history
 *
 * Copyright (c) 2010 Authors
 * Licensed under the GNU GPL version 3.0 or later.  See the file LICENSE for details.
 *
 */
import { createWebHashHistory, createRouter } from 'vue-router'
const routes = [
    {
        path: '/simulator',
        name: 'simulator',
        component: () => import('../components/Simulator.vue')
    },
    {
        path: '/:pathMatch(.*)*',
        name: 'NotFound',
        component: () => import('../components/NotFound.vue')
    },
]
const router = createRouter({
    history: createWebHashHistory(),
    routes
})
// Sets title for each routes
const DEFAULT_TITLE = 'Ink/Stitch';

router.beforeEach((to) => {
  document.title = to.meta.title || DEFAULT_TITLE
})
export default router
