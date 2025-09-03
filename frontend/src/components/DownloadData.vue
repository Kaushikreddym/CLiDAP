<!-- src/components/DownloadButton.vue -->
<template>
  <div>
    <v-btn color="success" @click="downloadCSV">
      Download CSV
    </v-btn>
    <v-btn color="primary" class="ml-2" :disabled="!lastCsv" @click="plotCSV">
      Plot
    </v-btn>
  </div>
</template>

<script setup>
import { computed, ref } from 'vue'
import { useAttrs, defineEmits } from 'vue'

const emit = defineEmits(['downloaded'])
const attrs = useAttrs()
const lastCsv = ref(null)

// Expected props: lat, lon, dataset, parameter, startDate, endDate
const lat = computed(() => attrs.lat)
const lon = computed(() => attrs.lon)
const dataset = computed(() => attrs.dataset)
const parameter = computed(() => attrs.parameter)
const startDate = computed(() => attrs.startDate)
const endDate = computed(() => attrs.endDate)

const downloadCSV = async () => {
  try {
    const url = new URL('http://localhost:8000/download_csv')
    url.searchParams.set('lat', lat.value)
    url.searchParams.set('lon', lon.value)
    url.searchParams.set('dataset', dataset.value)
    url.searchParams.set('parameter', parameter.value)
    url.searchParams.set('start_date', startDate.value)
    url.searchParams.set('end_date', endDate.value)

    const response = await fetch(url.toString())
    if (!response.ok) throw new Error('Failed to download CSV')

    const blob = await response.blob()
    const text = await blob.text()
    lastCsv.value = text
    emit('downloaded', text) // Emit CSV text to parent

    // Download as file
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = `${parameter.value}_${dataset.value}_lat${lat.value}_lon${lon.value}_${startDate.value}-${endDate.value}.csv`
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (err) {
    console.error('CSV download failed:', err)
    alert('Could not download CSV.')
  }
}

function plotCSV() {
  if (lastCsv.value) {
    emit('downloaded', lastCsv.value)
  }
}
</script>
