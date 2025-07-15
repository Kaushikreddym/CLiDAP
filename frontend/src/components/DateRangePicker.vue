<template>
  <div class="date-range-picker">
    <label>Start Date:</label>
    <Datepicker
      v-model="start"
      :format="format"
      :input-class="'date-input'"
      placeholder="Select start date"
      :clearable="true"
      :editable="true"
    />

    <label>End Date:</label>
    <Datepicker
      v-model="end"
      :format="format"
      :input-class="'date-input'"
      placeholder="Select end date"
      :clearable="true"
      :editable="true"
    />
  </div>
</template>

<script setup>
import { ref, watch, defineProps, defineEmits } from 'vue'
import Datepicker from '@vuepic/vue-datepicker'
import '@vuepic/vue-datepicker/dist/main.css'

const props = defineProps({
  startDate: String,
  endDate: String,
})
const emit = defineEmits(['update:dates'])

const start = ref(props.startDate || '')
const end = ref(props.endDate || '')
const format = 'yyyy-MM-dd'

// Keep local state in sync with parent props
watch(() => props.startDate, val => { start.value = val || '' })
watch(() => props.endDate, val => { end.value = val || '' })

// Emit updates to parent on change
watch([start, end], ([newStart, newEnd]) => {
  if (newStart && newEnd) {
    emit('update:dates', { start: newStart, end: newEnd })
  } else {
    emit('update:dates', null)
  }
})
</script>

<style scoped>
.date-range-picker {
  display: flex;
  flex-direction: column;
  gap: 1rem;
}

.date-input {
  width: 200px;
  padding: 0.3rem 0.5rem;
  font-size: 1rem;
}
</style>