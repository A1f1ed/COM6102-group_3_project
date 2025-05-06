import App from './App'

// #ifndef VUE3
import Vue from 'vue'
Vue.config.productionTip = false
App.mpType = 'app'
const app = new Vue({
    ...App
})
app.$mount()
// #endif

// #ifdef VUE3
import { createSSRApp } from 'vue'
export function createApp() {
  const app = createSSRApp(App)
  return {
    app
  }
}
// #endif

// 新增下方代码
import uView from "@/uni_modules/uview-ui"
Vue.use(uView)






//继续新增代码，引入api.js文件
import res from "api/api.js"
Vue.prototype.$uni = res.request