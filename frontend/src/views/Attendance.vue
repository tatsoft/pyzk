<template>
  <v-card>
    <v-tabs v-model="tab" grow :class="rtlClass">
      <v-tab value="inout">{{ $t('inout') }}</v-tab>
      <v-tab value="summary">{{ $t('summary') }}</v-tab>
    </v-tabs>
    <v-window v-model="tab">
      <v-window-item value="inout">
        <v-card-text :class="rtlClass">
          <div>{{ $t('attendance_inout_placeholder') }}</div>
        </v-card-text>
      </v-window-item>
      <v-window-item value="summary">
        <v-card-text :class="rtlClass">
          <div>{{ $t('attendance_summary_placeholder') }}</div>
        </v-card-text>
      </v-window-item>
    </v-window>
  </v-card>
</template>

<script setup>
import { ref, computed } from 'vue'
import { useI18n } from 'vue-i18n'
const tab = ref('inout')
const { locale, t } = useI18n()
const isArabic = computed(() => locale.value === 'ar')
const rtlClass = computed(() => isArabic.value ? 'text-end' : 'text-start')
</script>
