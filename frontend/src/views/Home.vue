<template>
  <v-card>
    <v-card-title :class="rtlClass">{{ $t('welcome') }}</v-card-title>
    <v-card-text :class="rtlClass">{{ $t('useSidebar') }}</v-card-text>
  </v-card>
</template>

<script setup>
import { computed } from 'vue'
import { useI18n } from 'vue-i18n'
const { locale } = useI18n()
const isArabic = computed(() => locale.value === 'ar')
const rtlClass = computed(() => isArabic.value ? 'text-end' : 'text-start')
</script>
