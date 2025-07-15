<!-- src/components/DownloadButton.vue -->
<template>
  <v-btn color="success" @click="downloadCSV">
    Download CSV
  </v-btn>
</template>

<script setup>
import { computed } from 'vue'
import { useAttrs } from 'vue'

const attrs = useAttrs()

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
    const link = document.createElement('a')
    link.href = URL.createObjectURL(blob)
    link.download = 'data.csv'
    document.body.appendChild(link)
    link.click()
    document.body.removeChild(link)
  } catch (err) {
    console.error('CSV download failed:', err)
    alert('Could not download CSV.')
  }
}
</script>
