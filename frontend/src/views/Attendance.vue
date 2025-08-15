<template>
  <v-card>
    <v-tabs v-model="tab" grow :class="rtlClass">
      <v-tab value="inout">{{ $t('inout') }}</v-tab>
      <v-tab value="summary">{{ $t('summary') }}</v-tab>
    </v-tabs>
    <v-window v-model="tab">
      <v-window-item value="inout">
        <v-card-text :class="rtlClass">
          <v-data-table
            :headers="headers"
            :items="attendance"
            :loading="loading"
            class="elevation-1"
            :no-data-text="$t('no_data')"
          />
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
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
const tab = ref('inout')
const { locale, t } = useI18n()
const isArabic = computed(() => locale.value === 'ar')
const rtlClass = computed(() => isArabic.value ? 'text-end' : 'text-start')

const attendance = ref([])
const loading = ref(false)
const headers = [
  { text: t('date') || 'Date', value: 'date' },
  { text: t('employee') || 'Employee', value: 'employee' },
  { text: t('in_time') || 'In Time', value: 'in_time' },
  { text: t('out_time') || 'Out Time', value: 'out_time' },
]

onMounted(async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:8000/attendance', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) throw new Error()
    attendance.value = await res.json()
  } catch (e) {
    attendance.value = []
  } finally {
    loading.value = false
  }
})
</script>
