<template>
  <v-app>
    <v-main>
      <v-container class="py-10">
        <h1 class="text-h4 font-weight-bold mb-6 text-center text-primary">
          CLiDAP - CLImate Data Access Portal
        </h1>

        <v-row dense>
          <v-col cols="12" md="6">
            <v-select
              v-model="selectedDataset"
              :items="datasets"
              label="Select Dataset"
              @update:modelValue="fetchVariables"
              outlined
              dense
              class="mb-4"
            />
          </v-col>

          <v-col cols="12" md="6">
            <v-select
              v-model="selectedVariable"
              :items="variables"
              label="Select Variable"
              outlined
              dense
              class="mb-4"
            />
          </v-col>
        </v-row>

        <v-row dense>
          <v-col cols="12" md="6">
            <DateRangeInput @update:dates="onDatesUpdate" />
            <div class="mt-2">
              <strong>Selected Range:</strong>
              <span>{{ startDate || '...' }}</span> to <span>{{ endDate || '...' }}</span>
            </div>
          </v-col>

          <v-col cols="12" md="6">
            <v-select
              v-model="subsetting"
              :items="['point', 'box']"
              label="Select Subsetting Type"
              outlined
              dense
              class="mb-4"
            />
          </v-col>
        </v-row>

        <v-row dense>
          <v-col cols="12" md="6" v-if="subsetting === 'point'">
            <PointInput
              :lat="pointLat"
              :lon="pointLon"
              @update:point="val => {
                pointLat = val.lat;
                pointLon = val.lon;
              }"
            />
          </v-col>

          <v-col cols="12" v-if="subsetting === 'box'">
            <MapBoxSelector @update:bounds="bounds = $event" />
          </v-col>
        </v-row>

        <v-divider class="my-6"></v-divider>

        <DownloadData
          :lat="pointLat"
          :lon="pointLon"
          :dataset="selectedDataset"
          :parameter="selectedVariable"
          :startDate="startDate"
          :endDate="endDate"
        />
      </v-container>
    </v-main>
  </v-app>
</template>

<script setup>
import { ref, onMounted } from 'vue'
import axios from 'axios'

import MapBoxSelector from './components/MapBoxSelector.vue'
import PointInput from './components/PointInput.vue'
import DownloadData from './components/DownloadData.vue'
import DateRangeInput from './components/DateRangeInput.vue'

const datasets = ref([])
const selectedDataset = ref(null)
const selectedVariable = ref(null)
const variables = ref([])

const subsetting = ref('point')
const pointLat = ref(51.1657)
const pointLon = ref(10.4515)
const startDate = ref(null)
const endDate = ref(null)
const bounds = ref([
  [9.5, 50.5],
  [11.5, 52.5],
])

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/datasets')
    datasets.value = res.data.datasets
  } catch (err) {
    console.error(err)
  }
})

const fetchVariables = async () => {
  if (!selectedDataset.value) return
  try {
    const res = await axios.get('http://localhost:8000/variables', {
      params: { dataset: selectedDataset.value }
    })
    variables.value = res.data.variables
  } catch (err) {
    console.error(err)
    variables.value = []
  }
}

function onDatesUpdate({ start, end }) {
  startDate.value = start
  endDate.value = end
}
</script>
<style scoped>
h1 {
  letter-spacing: 0.5px;
}

.mt-2 {
  margin-top: 0.5rem;
}

.v-container {
  background-color: #f9f9f9;
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0,0,0,0.05);
}
</style>