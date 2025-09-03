// frontend/src/main.js
import { createApp } from 'vue'
import App from './App.vue'
// import AppMap from './app_map.vue'
import { createVuetify } from 'vuetify'
import * as components from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import 'leaflet/dist/leaflet.css'
// import Markdown from 'vite-plugin-md'

// export default {
//   plugins: [Markdown()],
// }
const vuetify = createVuetify({
  components,
  directives,
})

createApp(App).use(vuetify).mount('#app')
