import { createApp } from 'vue'
import App from './App.vue'
import { createRouter, createWebHistory } from 'vue-router'

import { createVuetify } from 'vuetify'
import { useI18n } from 'vue-i18n'
import {
	VApp,
	VAppBar,
	VAppBarNavIcon,
	VNavigationDrawer,
	VList,
	VListItem,
	VIcon,
	VToolbarTitle,
	VBtn,
	VSpacer,
	VMain,
	VContainer,
	VRow,
	VCol,
	VTabs,
	VTab,
	VCard,
	VCardTitle,
	VCardText
} from 'vuetify/components'
import * as directives from 'vuetify/directives'
import 'vuetify/styles'
import '@mdi/font/css/materialdesignicons.css'
import routes from './routes'
import i18n from './i18n'

const vuetify = createVuetify({
	components: {
		VApp,
		VAppBar,
		VAppBarNavIcon,
		VNavigationDrawer,
		VList,
		VListItem,
		VIcon,
		VToolbarTitle,
		VBtn,
		VSpacer,
		VMain,
		VContainer,
		VRow,
		VCol,
		VTabs,
		VTab,
		VCard,
		VCardTitle,
		VCardText
	},
	directives,
	theme: {
		defaultTheme: 'dark',
		themes: {
			light: {},
			dark: {},
		},
	},
	rtl: {
		locale: {
			ar: true,
			en: false,
		},
		defaultLocale: 'en',
	},
})

const router = createRouter({
	history: createWebHistory(),
	routes,
})

createApp(App)
	.use(router)
	.use(vuetify)
	.use(i18n)
	.mount('#app')
