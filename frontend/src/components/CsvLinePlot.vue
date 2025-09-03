<template>
  <div v-if="plotReady">
    <div ref="plotDiv"></div>
  </div>
</template>

<script setup>
import { ref, watch } from 'vue'
import Papa from 'papaparse'
import Plotly from 'plotly.js-dist-min'

const props = defineProps({
  csv: String
})

const plotDiv = ref(null)
const plotReady = ref(false)

watch(() => props.csv, (csv) => {
  console.log('CsvLinePlot received CSV:', csv)
  if (!csv) return

  const parsed = Papa.parse(csv, { header: true })
  const rawData = parsed.data

  const timeCol = 'time'
  const valueCol = 'value'

  const data = rawData.filter(row =>
    row && row[timeCol] && row[valueCol] !== undefined && row[valueCol] !== ''
  )

  if (!data.length) return

  const x = data.map(row => row[timeCol])
  const y = data.map(row => Number(row[valueCol]))

  if (plotDiv.value) {
    Plotly.purge(plotDiv.value)
    Plotly.newPlot(plotDiv.value, [{
      x,
      y,
      type: 'scatter',
      mode: 'lines+markers',
      name: 'value'
    }], {
      title: 'Value over time',
      xaxis: { title: 'Time' },
      yaxis: { title: 'Value' }
    }, { responsive: true })

    plotReady.value = true
  }
})
</script>
