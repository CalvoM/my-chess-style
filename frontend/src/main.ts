import './assets/main.css'

import { createApp } from 'vue'
import { createPinia } from 'pinia'

import App from './App.vue'
import router from './router'

import PrimeVue from 'primevue/config'
import Aura from '@primeuix/themes/lara'
import Button from 'primevue/button'
import Card from 'primevue/card'
import Avatar from 'primevue/avatar'
import ToggleSwitch from 'primevue/toggleswitch'
import InputText from 'primevue/inputtext'
import Tabs from 'primevue/tabs'
import TabList from 'primevue/tablist'
import Tab from 'primevue/tab'
import TabPanels from 'primevue/tabpanels'
import TabPanel from 'primevue/tabpanel'
import FileUpload from 'primevue/fileupload'
import  Toast  from 'primevue/toast'
import ToastService from 'primevue/toastservice'
import Select from 'primevue/select'

const app = createApp(App)

app.component('Button', Button)
app.component('Card', Card)
app.component('Avatar', Avatar)
app.component('ToggleSwitch', ToggleSwitch)
app.component('Tabs', Tabs)
app.component('Tab', Tab)
app.component('TabList', TabList)
app.component('TabPanels', TabPanels)
app.component('TabPanel', TabPanel)
app.component('InputText', InputText)
app.component('FileUpload', FileUpload)
app.component('Toast', Toast)
app.component('Select', Select)

app.use(createPinia())
app.use(router)
app.use(ToastService)
app.use(PrimeVue, {
  theme: {
    preset: Aura,
    options: {
      darkModeSelector: false || 'none',
    },
  },
})

app.mount('#app')
