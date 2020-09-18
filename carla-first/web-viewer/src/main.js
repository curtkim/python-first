import Vue from 'vue'
import App from './App.vue'
import { Button, Slider } from 'element-ui';

Vue.use(Button)
Vue.use(Slider)

Vue.config.productionTip = false

new Vue({
  render: h => h(App),
}).$mount('#app')
