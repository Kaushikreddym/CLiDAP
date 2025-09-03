<template>
  <div class="cmip6-options">
    <h2 class="text-h5 font-weight-bold mb-4">CMIP6 Data Download</h2>
    <v-row dense>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="startTime"
          label="Start Time (YYYY-MM-DD)"
          outlined
          dense
          class="mb-2"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="endTime"
          label="End Time (YYYY-MM-DD)"
          outlined
          dense
          class="mb-2"
        />
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="12" md="6">
        <v-select
          v-model="experiment"
          :items="experiments"
          label="Experiment"
          outlined
          dense
          class="mb-2"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-select
          v-model="model"
          :items="models"
          label="Model"
          outlined
          dense
          class="mb-2"
          :disabled="!experiment"
        />
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="lat"
          label="Latitude"
          outlined
          dense
          class="mb-2"
          type="number"
        />
      </v-col>
      <v-col cols="12" md="6">
        <v-text-field
          v-model="lon"
          label="Longitude"
          outlined
          dense
          class="mb-2"
          type="number"
        />
      </v-col>
    </v-row>
    <v-row dense>
      <v-col cols="12" md="6">
        <v-select
          v-model="variable"
          :items="variables"
          label="Variable"
          outlined
          dense
          class="mb-2"
        />
      </v-col>
      <v-col cols="12" md="6" class="d-flex align-end">
        <v-btn color="primary" @click="downloadData">
          Download
        </v-btn>
      </v-col>
    </v-row>
  </div>
</template>

<script setup>
import { ref } from 'vue'

const startTime = ref('')
const endTime = ref('')
const experiment = ref('')
const model = ref('')
const lat = ref('')
const lon = ref('')
const variable = ref('')

const experiments = [
  'historical',
  'ssp126',
  'ssp245',
  'ssp370',
  'ssp585'
]
const models = [
  'GFDL-ESM4',
  'MPI-ESM1-2-HR',
  'UKESM1-0-LL',
  'CNRM-ESM2-1'
]
const variables = [
  'tas',
  'pr',
  'psl',
  'sfcWind'
]

async function downloadData() {
  const params = {
    experiment_id: experiment.value,
    source_id: model.value,
    variable_id: variable.value,
    lat: lat.value,
    lon: lon.value,
    start_time: startTime.value,
    end_time: endTime.value
  }
  try {
    const response = await fetch('http://localhost:8000/cmip6_download', {
      method: 'POST',
      headers: { 'Content-Type': 'application/json' },
      body: JSON.stringify(params)
    })
    if (!response.ok) throw new Error('Download failed')
    const blob = await response.blob()
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `${variable.value}_${model.value}_${experiment.value}_${startTime.value}_${endTime.value}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (err) {
    alert('Download failed: ' + err)
  }
}
</script>

<style scoped>
.cmip6-options {
  background: #f5f7fa;
  border-radius: 8px;
  padding: 2rem;
}
</style>