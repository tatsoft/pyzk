import Home from './views/Home.vue'
import Attendance from './views/Attendance.vue'
import Admin from './views/Admin.vue'
import Settings from './views/Settings.vue'

export default [
  { path: '/', name: 'Home', component: Home },
  { path: '/attendance', name: 'Attendance', component: Attendance },
  { path: '/admin', name: 'Admin', component: Admin },
  { path: '/settings', name: 'Settings', component: Settings },
]
