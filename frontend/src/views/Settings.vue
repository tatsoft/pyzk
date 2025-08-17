<template>
  <v-container>
    <v-row>
      <v-col cols="12">
        <h2>Settings</h2>
        <v-tabs v-model="tab">
          <v-tab>App Settings</v-tab>
          <v-tab>Device Settings</v-tab>
        </v-tabs>
        <v-window v-model="tab">
          <v-window-item>
            <v-card flat>
              <v-card-title>App Settings</v-card-title>
              <v-card-text>
                <v-btn color="success" @click="saveAppSettings" class="ml-2">Save Settings</v-btn>
                <v-alert v-if="settingsError" type="error" class="mt-2">{{ settingsError }}</v-alert>
                <v-form ref="appSettingsForm" class="mt-4">
                  <v-row>
                    <v-col cols="6">
                      <v-text-field v-model="settings.app.in_start" label="In Start (HH:MM)" required></v-text-field>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field v-model="settings.app.in_end" label="In End (HH:MM)" required></v-text-field>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field v-model="settings.app.out_start" label="Out Start (HH:MM)" required></v-text-field>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field v-model="settings.app.out_end" label="Out End (HH:MM)" required></v-text-field>
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </v-window-item>
          <v-window-item>
            <v-card flat>
              <v-card-title>Device Settings</v-card-title>
              <v-card-text>
                <v-btn color="success" @click="saveDeviceSettings" class="ml-2">Save Settings</v-btn>
                <v-alert v-if="settingsError" type="error" class="mt-2">{{ settingsError }}</v-alert>
                <v-form ref="deviceSettingsForm" class="mt-4">
                  <v-row>
                    <v-col cols="6">
                      <v-text-field v-model="settings.device.ip" label="Device IP" required></v-text-field>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field v-model="settings.device.port" label="Device Port" type="number" required></v-text-field>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field v-model="settings.device.name" label="Device Name"></v-text-field>
                    </v-col>
                    <v-col cols="6">
                      <v-text-field v-model="settings.device.location" label="Device Location"></v-text-field>
                    </v-col>
                  </v-row>
                </v-form>
              </v-card-text>
            </v-card>
          </v-window-item>
        </v-window>
      </v-col>
    </v-row>
  </v-container>
</template>

<script>
import axios from 'axios';

export default {
  data() {
    return {
  tab: 0,
      settings: {
        app: {
          in_start: '',
          in_end: '',
          out_start: '',
          out_end: ''
        },
        device: {
          ip: '',
          port: '',
          name: '',
          location: ''
        }
      },
      settingsError: ''
    };
  },
  methods: {
    async loadSettings() {
      try {
        const res = await axios.get('/api/settings.json');
        const defaultApp = { in_start: '', in_end: '', out_start: '', out_end: '' };
        const defaultDevice = { ip: '', port: '', name: '', location: '' };
        this.settings = {
          app: { ...defaultApp, ...(res.data && res.data.app ? res.data.app : {}) },
          device: { ...defaultDevice, ...(res.data && res.data.device ? res.data.device : {}) }
        };
        this.settingsError = '';
      } catch (e) {
        this.settingsError = 'Failed to load settings.json';
      }
    },
    async saveAppSettings() {
      try {
        await axios.post('/api/settings.json', {
          app: this.settings.app,
          device: this.settings.device
        });
        this.settingsError = '';
      } catch (e) {
        this.settingsError = 'Failed to save app settings.';
      }
    },
    async saveDeviceSettings() {
      try {
        await axios.post('/api/settings.json', {
          app: this.settings.app,
          device: this.settings.device
        });
        this.settingsError = '';
      } catch (e) {
        this.settingsError = 'Failed to save device settings.';
      }
    }
  },
  mounted() {
    this.loadSettings();
  }
};
</script>

<style scoped>
.mt-2 { margin-top: 16px; }
.mt-4 { margin-top: 32px; }
.ml-2 { margin-left: 16px; }
</style>
