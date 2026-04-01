<template>
  <v-card>
    <v-card-title :class="rtlClass">{{ $t('adminPanel') }}</v-card-title>
    <v-tabs v-model="tab" grow :class="rtlClass">
      <v-tab value="employees">{{ $t('employees') }}</v-tab>
      <v-tab value="shifts">{{ $t('shifts') }}</v-tab>
      <v-tab value="schedules">{{ $t('schedules') }}</v-tab>
      <v-tab value="holidays">{{ $t('holidays') }}</v-tab>
      <v-tab value="leaves">{{ $t('leaves') }}</v-tab>
      <v-tab value="import">Import Data</v-tab>
    </v-tabs>
    <v-window v-model="tab">
      <v-window-item value="employees">
        <v-card-text :class="rtlClass">
          <div class="mb-4">
            <v-btn @click="loadEmployees" :loading="empLoading" color="info" class="mr-2">
              <v-icon>mdi-refresh</v-icon>
              Refresh
            </v-btn>
            <span class="ml-4">Total Employees: {{ totalEmployees }}</span>
          </div>
          <v-data-table
            :headers="empHeaders"
            :items="employees"
            :loading="empLoading"
            class="elevation-1"
            :no-data-text="$t('no_data')"
            :items-per-page="25"
            :footer-props="{
              'items-per-page-options': [10, 25, 50, 100],
              'show-current-page': true,
              'show-first-last-page': true
            }"
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
          <h3>Import Data from Device</h3>
          <p>Device: {{ deviceIp }}</p>
          
          <h4 class="mt-4">Users</h4>
          <p>Import all users from the ZK device into the system</p>
          <v-btn @click="importUsers" :loading="importUsersLoading" color="info" class="mt-2 mr-2">
            <v-icon>mdi-account-multiple-plus</v-icon>
            Import Users
          </v-btn>
          <v-alert v-if="importUsersMessage" :type="importUsersSuccess ? 'success' : 'error'" class="mt-2">
            {{ importUsersMessage }}
          </v-alert>
          
          <h4 class="mt-6">Attendance Logs</h4>
          <p>Import all attendance logs from the ZK device into the system</p>
          <v-btn @click="importLogs" :loading="importLoading" color="primary" class="mt-2">
            <v-icon>mdi-download</v-icon>
            Import Logs
          </v-btn>
          <v-alert v-if="importMessage" :type="importSuccess ? 'success' : 'error'" class="mt-2">
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
const totalEmployees = ref(0)
const empHeaders = [
  { text: 'ID', value: 'id', width: '80px' },
  { text: 'Code', value: 'code', width: '120px' },
  { text: 'Name', value: 'name' },
  { text: 'Department', value: 'department' },
]

// Import logs state
const importLoading = ref(false)
const importMessage = ref('')
const importSuccess = ref(false)

// Import users state
const importUsersLoading = ref(false)
const importUsersMessage = ref('')
const importUsersSuccess = ref(false)

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
    importMessage.value = result.message || 'Import process started'
  } catch (e) {
    importSuccess.value = false
    importMessage.value = `Error: ${e.message}`
  } finally {
    importLoading.value = false
  }
}

async function importUsers() {
  importUsersLoading.value = true
  importUsersMessage.value = ''
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:8000/import-users/', {
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
    importUsersSuccess.value = true
    importUsersMessage.value = result.message || 'User import process started'
  } catch (e) {
    importUsersSuccess.value = false
    importUsersMessage.value = `Error: ${e.message}`
  } finally {
    importUsersLoading.value = false
  }
}

async function loadEmployees() {
  empLoading.value = true
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:8000/employees-simple/?skip=0&limit=10000', {
      headers: { 'Authorization': `Bearer ${token}` }
    })
    if (!res.ok) throw new Error()
    employees.value = await res.json()
    totalEmployees.value = employees.value.length
  } catch (e) {
    console.error(e)
    employees.value = []
    totalEmployees.value = 0
  } finally {
    empLoading.value = false
  }
}

onMounted(() => {
  loadEmployees()
})
</script>
