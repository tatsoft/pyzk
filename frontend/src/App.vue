<template>
  <v-app>
    <v-navigation-drawer app v-model="drawer" :clipped="$vuetify.display.mdAndUp" :location="isArabic ? 'right' : 'left'">
      <v-list>
        <v-list-item v-for="item in navItems" :key="item.text" :to="item.to" link>
          <v-list-item-icon>
            <v-icon>{{ item.icon }}</v-icon>
          </v-list-item-icon>
          <v-list-item-content>
            <v-list-item-title>{{ $t(item.text) }}</v-list-item-title>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-navigation-drawer>
    <v-app-bar app color="primary" dark>
      <v-app-bar-nav-icon @click="drawer = !drawer" />
      <v-toolbar-title>{{ $t('welcome') }}</v-toolbar-title>
      <v-spacer />
      <v-btn icon @click="toggleLang">
        <v-icon>{{ isArabic ? 'mdi-translate' : 'mdi-translate' }}</v-icon>
      </v-btn>
      <span style="margin-inline-start: 8px;">{{ isArabic ? 'العربية' : 'EN' }}</span>
      <v-btn icon @click="toggleTheme">
        <v-icon>{{ isDark ? 'mdi-white-balance-sunny' : 'mdi-weather-night' }}</v-icon>
      </v-btn>
    </v-app-bar>
    <v-main>
      <v-container fluid>
        <router-view />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
import { useTheme } from 'vuetify'
const drawer = ref(false)
const navItems = [
  { text: 'home', to: '/', icon: 'mdi-home' },
  { text: 'attendance', to: '/attendance', icon: 'mdi-calendar-check' },
  { text: 'admin', to: '/admin', icon: 'mdi-account-cog' },
  { text: 'settings', to: '/settings', icon: 'mdi-cog' },
]
const { locale } = useI18n()
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
</style>
