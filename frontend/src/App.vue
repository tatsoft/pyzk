<template>
  <v-app>
    <template v-if="$route.path !== '/login'">
      <v-navigation-drawer app v-model="drawer" :clipped="$vuetify.display.mdAndUp" :location="isArabic ? 'right' : 'left'">
        <v-list>
          <v-list-item
            v-for="item in navItems"
            :key="item.text"
            :to="item.to"
            link
            :prepend-icon="item.icon"
            :title="$t(item.text)"
            :class="isArabic ? 'text-end' : 'text-start'"
          />
        </v-list>
      </v-navigation-drawer>
      <v-app-bar app color="primary" dark :class="{ 'rtl-bar': isArabic }">
        <div class="app-bar-content" :class="{ 'flex-row-reverse': isArabic }">
          <v-app-bar-nav-icon @click="drawer = !drawer" />
          <v-toolbar-title>{{ $t('welcome') }}</v-toolbar-title>
          <v-spacer />
          <span v-if="username" class="mx-2">{{ username }}</span>
          <!-- Connectivity indicators -->
          <span title="Database status" style="margin-right:8px;">
            <v-icon :color="dbStatus === 'ok' ? 'green' : 'red'">mdi-database</v-icon>
          </span>
          <span title="Device status" style="margin-right:8px;">
            <v-icon :color="deviceStatus === 'ok' ? 'green' : 'red'">mdi-usb</v-icon>
          </span>
          <v-btn icon @click="logout" v-if="username">
            <v-icon>mdi-logout</v-icon>
          </v-btn>
          <v-btn icon @click="toggleLang">
            <v-icon>{{ isArabic ? 'mdi-translate' : 'mdi-translate' }}</v-icon>
          </v-btn>
          <span style="margin-inline-start: 8px;">{{ isArabic ? 'العربية' : 'EN' }}</span>
          <v-btn icon @click="toggleTheme">
            <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
          </v-btn>
        </div>
      </v-app-bar>
    </template>
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { onMounted } from 'vue'
const dbStatus = ref('unknown')
const deviceStatus = ref('unknown')

async function checkStatus() {
  try {
    const res = await fetch('http://localhost:8000/health/db')
    dbStatus.value = res.ok ? 'ok' : 'fail'
  } catch { dbStatus.value = 'fail' }
  try {
    const res = await fetch('http://localhost:8000/health/device')
    deviceStatus.value = res.ok ? 'ok' : 'fail'
  } catch { deviceStatus.value = 'fail' }
}
onMounted(() => {
  checkStatus()
  setInterval(checkStatus, 5000)
})
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useTheme } from 'vuetify'
const drawer = ref(false)
const navItems = computed(() => {
  const items = [
    { text: 'home', to: '/', icon: 'mdi-home' },
    { text: 'attendance', to: '/attendance', icon: 'mdi-calendar-check' },
  ]
  if (isAdmin.value) {
    items.push({ text: 'admin', to: '/admin', icon: 'mdi-account-cog' })
    items.push({ text: 'settings', to: '/settings', icon: 'mdi-cog' })
  }
  return items
})
import { useRouter } from 'vue-router'
const { locale } = useI18n()
// JWT decode helper
function parseJwt (token) {
  try {
    return JSON.parse(atob(token.split('.')[1]))
  } catch (e) { return {} }
}


const userPayload = computed(() => {
  const token = localStorage.getItem('token')
  if (!token) return {}
  return parseJwt(token)
})
const username = computed(() => userPayload.value?.sub || userPayload.value?.username || '')
const isAdmin = computed(() => userPayload.value?.is_admin === true || userPayload.value?.is_admin === 1)

const router = useRouter()
function logout() {
  localStorage.removeItem('token')
  router.push('/login')
}
const isArabic = computed(() => locale.value === 'ar')
const toggleLang = () => {
  locale.value = isArabic.value ? 'en' : 'ar'
}

// Dynamically set <html> dir attribute for true RTL/LTR
import { watchEffect } from 'vue'
watchEffect(() => {
  document.documentElement.setAttribute('dir', isArabic.value ? 'rtl' : 'ltr')
})


const theme = useTheme()
const isDark = computed(() => theme.global.current.value.dark)
const toggleTheme = () => {
  theme.global.name.value = isDark.value ? 'light' : 'dark'
}
</script>

<style>
html, body, #app {
  height: 100%;
}
  .app-bar-content {
    display: flex;
    align-items: center;
    width: 100%;
  }
  .flex-row-reverse {
    flex-direction: row-reverse;
  }
</style>
