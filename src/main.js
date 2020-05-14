import Vue from 'vue'
import App from './App.vue'
import VueRouter from 'vue-router'
import Mint from 'mint-ui'
import 'mint-ui/lib/style.css'

Vue.use(Mint)

Vue.use(VueRouter)

import VueResource from 'vue-resource'

Vue.use(VueResource)

import { MessageBox } from 'mint-ui'
import { ajax } from './script/ajax.js'
import { Toast } from 'mint-ui';
import { config } from './script/config.js'

import login from './component/login.vue'
import home from './component/home.vue'
import reg from './component/reg.vue'
import article from './component/article.vue'
import new_article from './component/new_article.vue'
import update_article from './component/update_article.vue'

const routes = [
  { path: '/article/:id', component: article },
  { path: '/new_article', component: new_article },
  { path: '/update_article/:id', component: update_article },
  { path: '/login', component: login },
  { path: '/home', component: home },
  { path: '/reg', component: reg },
  { path: '/', component: login }
]

const router = new VueRouter({ routes })

new Vue({
  el: '#app',
  router,
  render: h => h(App)
})
