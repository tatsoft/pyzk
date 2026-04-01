<template>
  <v-card>
    <v-card-title :class="rtlClass">{{ $t('adminPanel') }}</v-card-title>
    <v-tabs v-model="tab" grow :class="rtlClass">
      <v-tab value="employees">{{ $t('employees') }}</v-tab>
      <v-tab value="shifts">{{ $t('shifts') }}</v-tab>
      <v-tab value="schedules">{{ $t('schedules') }}</v-tab>
      <v-tab value="holidays">{{ $t('holidays') }}</v-tab>
      <v-tab value="leaves">{{ $t('leaves') }}</v-tab>
      <v-tab value="import">Import Logs</v-tab>
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
      <v-window-item value="import">
        <v-card-text :class="rtlClass">
          <h3>Import Attendance Logs from Device</h3>
          <p>Click the button below to import attendance logs from the ZK device ({{ deviceIp }})</p>
          <v-btn @click="importLogs" :loading="importLoading" color="primary" class="mt-4">
            <v-icon>mdi-download</v-icon>
            Import Logs
          </v-btn>
          <v-alert v-if="importMessage" :type="importSuccess ? 'success' : 'error'" class="mt-4">
            {{ importMessage }}
          </v-alert>
        </v-card-text>
      </v-window-item>
    </v-window>
  </v-card>
</template>

<script setup>
import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import { authFetch } from '../api'
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

// Import logs state
const importLoading = ref(false)
const importMessage = ref('')
const importSuccess = ref(false)
const deviceIp = ref('192.168.8.201')

async function importLogs() {
  importLoading.value = true
  importMessage.value = ''
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:8000/import-logs/', {
      method: 'POST',
      headers: {
        'Authorization': `Bearer ${token}`,
        'Content-Type': 'application/json'
      }
    })
    if (!res.ok) {
      const error = await res.json()
      throw new Error(error.detail || 'Import failed')
    }
    const result = await res.json()
    importSuccess.value = true
    importMessage.value = `Successfully imported ${result.imported} records and updated ${result.updated} records. Total processed: ${result.total_processed}`
  } catch (e) {
    importSuccess.value = false
    importMessage.value = `Error: ${e.message}`
  } finally {
    importLoading.value = false
  }
}

onMounted(async () => {
  empLoading.value = true
  try {
    const res = await authFetch('http://localhost:8000/employees');
    if (!res.ok) throw new Error()
    employees.value = await res.json()
  } catch (e) {
    employees.value = []
  } finally {
    empLoading.value = false
  }
})
</script>
