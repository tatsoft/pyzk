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
          <div>
            <h3>{{ $t('summary') }}</h3>
            <ul>
              <li>{{ $t('total_records') }}: {{ totalRecords }}</li>
              <li>{{ $t('unique_employees') }}: {{ uniqueEmployees }}</li>
              <li>{{ $t('earliest_date') }}: {{ earliestDate }}</li>
              <li>{{ $t('latest_date') }}: {{ latestDate }}</li>
              <li>{{ $t('present_count') }}: {{ presentCount }}</li>
            </ul>
            <h4>{{ $t('employee_statistics') }}</h4>
            <v-data-table
              :headers="empStatsHeaders"
              :items="employeeStats"
              class="elevation-1 mb-6"
              :no-data-text="$t('no_data')"
              dense
            />
            <h4>{{ $t('daily_attendance') }}</h4>
            <AttendanceBarChart v-if="dailyChartData" :chartData="dailyChartData" :chartOptions="chartOptions" />
            <h4>{{ $t('weekly_attendance') }}</h4>
            <AttendanceBarChart v-if="weeklyChartData" :chartData="weeklyChartData" :chartOptions="chartOptions" />
            <h4>{{ $t('monthly_attendance') }}</h4>
            <AttendanceBarChart v-if="monthlyChartData" :chartData="monthlyChartData" :chartOptions="chartOptions" />
<!-- Per-employee statistics are now in <script setup> -->
          </div>
        </v-card-text>
      </v-window-item>
    </v-window>
  </v-card>
</template>

<script setup>

import { ref, computed, onMounted } from 'vue'
import { useI18n } from 'vue-i18n'
import AttendanceBarChart from '../components/AttendanceBarChart.js'
const tab = ref('inout')
const { locale, t } = useI18n()
const isArabic = computed(() => locale.value === 'ar')
const rtlClass = computed(() => isArabic.value ? 'text-end' : 'text-start')

const attendance = ref([])
const loading = ref(false)
const headers = [
  { text: t('date') || 'Date', value: 'date' },
  { text: t('employee') || 'Employee', value: 'employee_name' },
  { text: t('in_time') || 'In Time', value: 'in_time' },
  { text: t('out_time') || 'Out Time', value: 'out_time' },
]

// Summary statistics
const totalRecords = computed(() => attendance.value.length)
const uniqueEmployees = computed(() => new Set(attendance.value.map(a => a.employee_name)).size)
const sortedDates = computed(() => attendance.value.map(a => a.date).filter(Boolean).sort())
const earliestDate = computed(() => sortedDates.value[0] || '-')
const latestDate = computed(() => sortedDates.value[sortedDates.value.length - 1] || '-')
const presentCount = computed(() => attendance.value.filter(a => a.in_time).length)

// Chart helpers
function groupBy(arr, fn) {
  return arr.reduce((acc, x) => {
    const k = fn(x)
    acc[k] = (acc[k] || 0) + 1
    return acc
  }, {})
}

const dailyChartData = computed(() => {
  if (!attendance.value.length) return null
  const grouped = groupBy(attendance.value, a => a.date)
  const labels = Object.keys(grouped).sort()
  return {
    labels,
    datasets: [{
      label: t('daily_attendance'),
      backgroundColor: '#1976d2',
      data: labels.map(l => grouped[l])
    }]
  }
})

const weeklyChartData = computed(() => {
  if (!attendance.value.length) return null
  // Get week string as YYYY-WW
  const grouped = groupBy(attendance.value, a => {
    const d = new Date(a.date)
    const year = d.getFullYear()
    const week = Math.ceil(((d.getTime() - new Date(year,0,1).getTime()) / 86400000 + new Date(year,0,1).getDay()+1) / 7)
    return `${year}-W${week}`
  })
  const labels = Object.keys(grouped).sort()
  return {
    labels,
    datasets: [{
      label: t('weekly_attendance'),
      backgroundColor: '#43a047',
      data: labels.map(l => grouped[l])
    }]
  }
})

const monthlyChartData = computed(() => {
  if (!attendance.value.length) return null
  // Get month string as YYYY-MM
  const grouped = groupBy(attendance.value, a => a.date?.slice(0,7))
  const labels = Object.keys(grouped).sort()
  return {
    labels,
    datasets: [{
      label: t('monthly_attendance'),
      backgroundColor: '#fbc02d',
      data: labels.map(l => grouped[l])
    }]
  }
})

const chartOptions = {
  responsive: true,
  plugins: {
    legend: { display: false },
    title: { display: false }
  },
  scales: {
    x: { title: { display: true, text: t('date') } },
    y: { title: { display: true, text: t('present_count') }, beginAtZero: true }
  }
}

// Employee statistics table headers
const empStatsHeaders = [
  { text: t('employee') || 'Employee', value: 'employee_name' },
  { text: t('present_days') || 'Present Days', value: 'present_days' }
]

// Compute employee statistics
const employeeStats = computed(() => {
  // Group attendance by employee_name and count present days (where in_time exists)
  const stats = {}
  for (const a of attendance.value) {
    if (!a.employee_name) continue
    if (!stats[a.employee_name]) stats[a.employee_name] = 0
    if (a.in_time) stats[a.employee_name] += 1
  }
  return Object.entries(stats).map(([employee_name, present_days]) => ({
    employee_name,
    present_days
  }))
})

// @ts-ignore
onMounted(async () => {
  loading.value = true
  try {
    const token = localStorage.getItem('token')
    const res = await fetch('http://localhost:8000/attendance_records/', {
      headers: { Authorization: `Bearer ${token}` }
    })
    if (!res.ok) throw new Error()
    const data = await res.json()
    // Map employee name if present, else show ID
    attendance.value = data.map(item => ({
      ...item,
      employee_name: item.employee?.name || item.employee_id || ''
    }))
  } catch (e) {
    attendance.value = []
  } finally {
    loading.value = false
  }
})

</script>
