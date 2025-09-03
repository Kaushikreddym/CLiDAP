<template>
  <v-app>
    <v-main>
      <div class="dashboard-bg">
        <v-container class="py-10">
          <v-card class="mb-6 elevation-3 dashboard-header" color="primary" dark>
            <v-row align="center">
              <v-col cols="auto">
                <v-icon size="36">mdi-weather-partly-cloudy</v-icon>
              </v-col>
              <v-col>
                <h1 class="text-h4 font-weight-bold mb-0">CLiDAP - CLImate Data Access Portal</h1>
              </v-col>
            </v-row>
          </v-card>

          <v-tabs v-model="activeTab" grow class="mb-6">
            <v-tab value="main">
              <span class="Visualization-tab">
                <v-icon left>mdi-weather-pouring</v-icon> Obs & Reanalysis
              </span>
            </v-tab>
            <v-tab value="cmip6">
              <span class="cmip6-tab">
                <v-icon left>mdi-database</v-icon> CMIP6
              </span>
            </v-tab>
            <v-tab value="Visualization">
              <span class="Visualization-tab">
                <v-icon left>mdi-chart-line</v-icon> Visualization
              </span>
            </v-tab>
              <v-tab value="docs">
                <span class="docs-tab">
                  <v-icon left>mdi-book-open-page-variant</v-icon> API Docs
                </span>
              </v-tab>
          </v-tabs>
          <v-window v-model="activeTab">
            <!-- Observations & Reanalysis Tab -->
            <v-window-item value="main">
              <v-card class="elevation-2 pa-6 mb-6">
                <v-alert v-if="errorMessage" type="error" dense class="mb-4">
                  {{ errorMessage }}
                </v-alert>

                <v-row dense>
                  <v-col cols="12" md="6">
                    <v-select
                      v-model="selectedDataset"
                      :items="datasets"
                      label="Select Dataset"
                      @update:modelValue="fetchVariables"
                      outlined dense class="mb-4"
                    />
                  </v-col>
                  <v-col cols="12" md="6">
                    <v-select
                      v-model="selectedVariable"
                      :items="variables"
                      label="Select Variable"
                      :disabled="!selectedDataset"
                      outlined dense class="mb-4"
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
                      outlined dense class="mb-4"
                    />
                  </v-col>
                </v-row>

                <v-row dense>
                  <v-col cols="12" md="6" v-if="subsetting === 'point'">
                    <PointInput
                      :lat="pointLat"
                      :lon="pointLon"
                      @update:point="val => {
                        pointLat = val.lat
                        pointLon = val.lon
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
                  @downloaded="csvData = $event"
                />

                <CsvLinePlot v-if="csvData" :csv="csvData" class="mt-6" />
              </v-card>
            </v-window-item>

            <!-- CMIP6 Tab -->
            <v-window-item value="cmip6">
              <v-card class="elevation-2 pa-6 cmip6-card">
                <CMIP6Options />
              </v-card>
            </v-window-item>
            <v-window-item value="docs">
              <v-card class="elevation-2 pa-6">
                <div class="markdown-body" v-html="readmeHtml"></div>
              </v-card>
            </v-window-item>
            <!-- <v-window-item value="plot">
              <v-card class="elevation-2 pa-6">
                <h2 class="text-h6 mb-4">Sample Plot</h2>
                <TestPlot />
              </v-card>
            </v-window-item> -->
            <v-footer app padless>
              <v-col class="text-center py-4" cols="12">
                <v-divider class="mb-3"></v-divider>
                <div class="text-subtitle-2">
                  © {{ new Date().getFullYear() }} CLiDAP |
                    <v-btn icon :href="'https://github.com/Kaushikreddym/CLiDAP'" target="_blank" variant="text">
                    <v-icon size="20">mdi-github</v-icon>
                  </v-btn> 
                  <a href="https://www.zalf.de/en/Pages/ZALF.aspx" target="_blank">Leibniz Centre for Agricultural Landscape Research (ZALF)</a>
                </div>
              </v-col>
            </v-footer>
          </v-window>
        </v-container>
      </div>
    </v-main>
  </v-app>

</template>

<script setup>
import { ref, onMounted, watch } from 'vue'
import axios from 'axios'

import MapBoxSelector from './components/MapBoxSelector.vue'
import PointInput from './components/PointInput.vue'
import DownloadData from './components/DownloadData.vue'
import DateRangeInput from './components/DateRangeInput.vue'
import CMIP6Options from './components/CMIP6Options.vue'
import CsvLinePlot from './components/CsvLinePlot.vue'
// import TestPlot from './components/TestPlot.vue'
import MarkdownIt from 'markdown-it'
import rawMarkdown from './assets/README.md?raw'  // ✅ Import as raw text

const md = new MarkdownIt()
const readmeHtml = ref(md.render(rawMarkdown))

const activeTab = ref('main')

const datasets = ref([])
const selectedDataset = ref(null)
const selectedVariable = ref(null)
const variables = ref([])
const csvData = ref(null)
const errorMessage = ref(null)

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
    errorMessage.value = 'Failed to load datasets.'
  }
})

const fetchVariables = async () => {
  selectedVariable.value = null
  variables.value = []
  if (!selectedDataset.value) return
  try {
    const res = await axios.get('http://localhost:8000/variables', {
      params: { dataset: selectedDataset.value }
    })
    variables.value = res.data.variables
  } catch (err) {
    console.error(err)
    variables.value = []
    errorMessage.value = 'Could not fetch variables.'
  }
}

function onDatesUpdate({ start, end }) {
  startDate.value = start
  endDate.value = end
}

// Reset CSV when parameters change
watch([
  selectedDataset,
  selectedVariable,
  startDate,
  endDate,
  pointLat,
  pointLon,
  subsetting
], () => {
  csvData.value = null
})
</script>

<style scoped>
.dashboard-bg {
  min-height: 100vh;
  background: linear-gradient(135deg, #e0eafc 0%, #cfdef3 100%);
}
.dashboard-header {
  border-radius: 16px;
  box-shadow: 0 4px 24px rgba(0, 0, 0, 0.08);
}
.cmip6-tab {
  display: flex;
  align-items: center;
  gap: 6px;
}
.cmip6-card {
  background: linear-gradient(120deg, #f5f7fa 60%, #e3e6ee 100%);
  border-radius: 16px;
}
.v-card {
  border-radius: 16px;
}
.mt-2 {
  margin-top: 0.5rem;
}
.v-container {
  border-radius: 12px;
  padding: 2rem;
  box-shadow: 0 2px 10px rgba(0, 0, 0, 0.05);
}
.plot-tab {
  display: flex;
  align-items: center;
  gap: 6px;
}
.dashboard-bg::before {
  content: "";
  position: absolute;
  top: 0; left: 0; right: 0; bottom: 0;
  background: 
    linear-gradient(45deg, rgba(0, 0, 0, 0.03) 25%, transparent 25%, transparent 75%, rgba(0, 0, 0, 0.03) 75%, rgba(0, 0, 0, 0.03)) 0 0 / 10px 10px,
    linear-gradient(-45deg, rgba(0, 0, 0, 0.01) 25%, transparent 25%, transparent 15%, rgba(0.1, 0, 0.1, 0.1) 75%, rgba(0, 0, 0, 0.03)) 0 0 / 10px 10px;
  z-index: 0;
}
.markdown-body {
  font-family: Roboto, sans-serif;
  font-size: 0.95rem;
  line-height: 1.6;
}
.markdown-body h1 {
  font-size: 1.5rem;
}
.markdown-body h2 {
  font-size: 1.2rem;
  margin-top: 1.5rem;
}
.markdown-body ul {
  padding-left: 1.5rem;
  margin-bottom: 1rem;
}
.markdown-body code {
  background: #f4f4f4;
  padding: 2px 4px;
  border-radius: 4px;
}
</style>