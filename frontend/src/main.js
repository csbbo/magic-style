import Vue from 'vue'
import App from './App.vue'
import router from "./router"
import store from './store'
import ajax from 'axios'
import ElementUI from 'element-ui'
import 'element-ui/lib/theme-chalk/index.css'
import * as Cookies from 'js-cookie'

import 'materialize-css/dist/js/materialize.js'
import 'materialize-css/dist/css/materialize.css'
import 'material-design-icons'

Vue.use(ElementUI)

ajax.get('/api/CSRFTokenAPI').then(() => {
  ajax.defaults.headers['X-CSRFToken'] = Cookies.get('csrftoken')
})

// window.$ = window.jQuery = require('jquery');
ajax.defaults.withCredentials = true
Vue.config.productionTip = false

new Vue({
  el: '#app',
  router,
  store,
  render: h => h(App),
}).$mount('#app')
