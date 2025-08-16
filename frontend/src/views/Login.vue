<template>
  <v-container class="fill-height d-flex align-center justify-center">
    <v-card width="400">
      <v-card-title class="text-center">{{ $t('login') }}</v-card-title>
      <v-card-text>
        <v-form @submit.prevent="onLogin">
          <v-text-field
            v-model="username"
            :label="$t('username')"
            prepend-inner-icon="mdi-account"
            required
          />
          <v-text-field
            v-model="password"
            :label="$t('password')"
            prepend-inner-icon="mdi-lock"
            type="password"
            required
          />
          <v-btn type="submit" color="primary" block :loading="loading">
            {{ $t('login') }}
          </v-btn>
          <v-alert v-if="error" type="error" class="mt-2">{{ error }}</v-alert>
        </v-form>
      </v-card-text>
    </v-card>
  </v-container>
</template>

<script setup>
import { ref } from 'vue'
import { useI18n } from 'vue-i18n'
const { t } = useI18n()
const username = ref('')
const password = ref('')
const loading = ref(false)
const error = ref('')

import { useRouter } from 'vue-router'
const router = useRouter()
const onLogin = async () => {
  loading.value = true
  error.value = ''
  try {
    const form = new URLSearchParams();
    form.append('username', username.value);
    form.append('password', password.value);
    const res = await fetch('http://localhost:8000/login', {
      method: 'POST',
      headers: { 'Content-Type': 'application/x-www-form-urlencoded' },
      body: form
    })
    if (!res.ok) throw new Error()
    const data = await res.json()
    if (data.access_token) {
      localStorage.setItem('token', data.access_token)
      router.push('/')
    } else {
      throw new Error()
    }
  } catch (e) {
    error.value = t('login_failed')
  } finally {
    loading.value = false
  }
}
</script>

<style scoped>
.fill-height {
  min-height: 100vh;
}
</style>
