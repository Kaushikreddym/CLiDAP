<template>
  <div>Hello, Vue is working!</div>
</template>
<script setup>
</script>

<!-- <template>
  <v-app>
    <v-main>
      <v-container class="py-10">
        <v-select
          v-model="selectedDataset"
          :items="datasets"
          label="Select Dataset"
          @update:modelValue="fetchVariables"
          outlined
          class="mb-4"
        />

        <v-select
          v-model="selectedVariable"
          :items="variables"
          label="Select Variable"
          outlined
          class="mb-4"
        />

        <div style="height: 400px;">
          <LMap
            style="height: 400px; width: 100%;"
            :zoom="zoom"
            :center="mapCenter"
            @update:bounds="onBoundsChange"
          >
            <LTileLayer :url="tileUrl" />
            <LRectangle :bounds="bounds" :color="'blue'" />
          </LMap>
        </div>

        <div class="mt-4">
          <p><strong>Bounds:</strong></p>
          <p>South: {{ bounds[0][0] }}, West: {{ bounds[0][1] }}</p>
          <p>North: {{ bounds[1][0] }}, East: {{ bounds[1][1] }}</p>
        </div>
      </v-container>
    </v-main>
  </v-app>
</template>


<script setup>
import axios from 'axios'
import { ref, onMounted } from 'vue'
// import 'leaflet/dist/leaflet.css'
import { LMap, LTileLayer, LRectangle } from 'vue3-leaflet'

const datasets = ref([])
const selectedDataset = ref(null)
const selectedVariable = ref(null)
const variables = ref([])

onMounted(async () => {
  try {
    const res = await axios.get('http://localhost:8000/datasets')
    datasets.value = res.data.datasets
  } catch (err) {
    console.error('Failed to fetch datasets:', err)
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
    console.error('Failed to fetch variables:', err)
    variables.value = []
  }
}

const zoom = ref(5)
const mapCenter = ref([51.1657, 10.4515])
const bounds = ref([
  [50.5, 9.5],
  [52.5, 11.5]
])
// const tileUrl = 'https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png'

const onBoundsChange = (newBounds) => {
  bounds.value = newBounds
}
</script>

<style scoped>
.v-container {
  max-width: 600px;
  margin: auto;
}
</style> -->

<template>
  <div ref="mapContainer" class="map-container"></div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount } from 'vue'
import Map from 'ol/Map'
import View from 'ol/View'
import TileLayer from 'ol/layer/Tile'
import OSM from 'ol/source/OSM'

const mapContainer = ref(null)
let map = null

onMounted(() => {
  map = new Map({
    target: mapContainer.value,
    layers: [
      new TileLayer({
        source: new OSM(),
      }),
    ],
    view: new View({
      center: [0, 0], // Coordinates in EPSG:3857 (Web Mercator)
      zoom: 2,
    }),
  })
})

onBeforeUnmount(() => {
  if (map) {
    map.setTarget(null)
  }
})
</script>

<style scoped>
.map-container {
  width: 100%;
  height: 400px;
}
</style>

