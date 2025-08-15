<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h2 :class="rtlClass">{{ $t('settings') }}</h2>
        <v-tabs v-model="tab" :class="rtlClass">
          <v-tab v-for="(label, i) in tabLabels" :key="i">{{ label }}</v-tab>
        </v-tabs>
        <v-tabs-items v-model="tab">
          <v-tab-item>
            <v-card flat>
              <v-card-title :class="rtlClass">{{ $t('users_and_roles') }}</v-card-title>
              <v-card-text :class="rtlClass">
                <p>{{ $t('manage_users_roles') }}</p>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card flat>
              <v-card-title :class="rtlClass">{{ $t('holidays') }}</v-card-title>
              <v-card-text :class="rtlClass">
                <p>{{ $t('manage_holidays') }}</p>
              </v-card-text>
            </v-card>
          </v-tab-item>
          <v-tab-item>
            <v-card flat>
              <v-card-title :class="rtlClass">{{ $t('app_settings') }}</v-card-title>
              <v-card-text :class="rtlClass">
                <p>{{ $t('manage_app_settings') }}</p>
              </v-card-text>
            </v-card>
          </v-tab-item>
        </v-tabs-items>
      </v-col>
    </v-row>
  </v-container>
</template>
