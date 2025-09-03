<template>
  <div ref="plotDiv" style="width: 100%; height: 400px;"></div>
</template>

<script setup>
import { onMounted, ref } from 'vue'
import Plotly from 'plotly.js-dist-min'

const plotDiv = ref(null)

onMounted(() => {
  Plotly.newPlot(plotDiv.value, [{
    x: [1, 2, 3],
    y: [10, 15, 13],
    type: 'scatter'
  }])
})
</script>