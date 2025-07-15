<template>
  <v-text-field
    v-model.number="lat"
    label="Latitude"
    type="number"
    step="0.0001"
    outlined
  />
  <v-text-field
    v-model.number="lon"
    label="Longitude"
    type="number"
    step="0.0001"
    outlined
  />
</template>

<script setup>
import { ref, watch, defineEmits, defineProps } from 'vue'

const emits = defineEmits(['update:point'])
const props = defineProps({
  lat: Number,
  lon: Number,
})

const lat = ref(props.lat || 0)
const lon = ref(props.lon || 0)

watch([lat, lon], () => {
  emits('update:point', { lat: lat.value, lon: lon.value })
})
</script>
