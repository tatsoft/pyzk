<template>
  <v-card>
    <v-card-title :class="rtlClass">{{ $t('adminPanel') }}</v-card-title>
    <v-tabs v-model="tab" grow :class="rtlClass">
      <v-tab value="employees">{{ $t('employees') }}</v-tab>
      <v-tab value="shifts">{{ $t('shifts') }}</v-tab>
      <v-tab value="schedules">{{ $t('schedules') }}</v-tab>
      <v-tab value="holidays">{{ $t('holidays') }}</v-tab>
      <v-tab value="leaves">{{ $t('leaves') }}</v-tab>
    </v-tabs>
    <v-window v-model="tab">
      <v-window-item value="employees">
        <v-card-text :class="rtlClass">
          <v-data-table
            :headers="empHeaders"
            :items="employees"
            :loading="empLoading"
            class="elevation-1"
            :no-data-text="$t('no_data')"
          />
        </v-card-text>
      </v-window-item>
      <v-window-item value="shifts">
        <v-card-text :class="rtlClass">{{ $t('admin_shifts_placeholder') }}</v-card-text>
      </v-window-item>
      <v-window-item value="schedules">
        <v-card-text :class="rtlClass">{{ $t('admin_schedules_placeholder') }}</v-card-text>
      </v-window-item>
      <v-window-item value="holidays">
        <v-card-text :class="rtlClass">{{ $t('admin_holidays_placeholder') }}</v-card-text>
      </v-window-item>
      <v-window-item value="leaves">
        <v-card-text :class="rtlClass">{{ $t('admin_leaves_placeholder') }}</v-card-text>
      </v-window-item>
    </v-window>
  </v-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
const tab = ref('employees')
const { locale, t } = useI18n()
const isArabic = computed(() => locale.value === 'ar')
const rtlClass = computed(() => isArabic.value ? 'text-end' : 'text-start')

const employees = ref([])
const empLoading = ref(false)
const empHeaders = [
  { text: t('username') || 'Username', value: 'username' },
  { text: t('name') || 'Name', value: 'name' },
  { text: t('role') || 'Role', value: 'role' },
]

onMounted(async () => {
  empLoading.value = true
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:8000/employees', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) throw new Error()
    employees.value = await res.json()
  } catch (e) {
    employees.value = []
  } finally {
    empLoading.value = false
  }
})
</script>
