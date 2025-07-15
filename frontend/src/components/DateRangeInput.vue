<!-- components/DateRangeInput.vue -->
<script setup>
import { ref, computed, defineEmits, watch } from 'vue'

const startDate = ref('')
const endDate = ref('')

const datePattern = /^\d{4}-\d{2}-\d{2}$/

const isStartDateValid = computed(() => datePattern.test(startDate.value))
const isEndDateValid = computed(() => datePattern.test(endDate.value))

const emit = defineEmits(['update:dates'])

// Whenever startDate or endDate changes, emit the updated values
watch([startDate, endDate], () => {
  emit('update:dates', { start: startDate.value, end: endDate.value })
})
</script>

<template>
  <label>
    Start Date:
    <input
      type="text"
      v-model="startDate"
      placeholder="YYYY-MM-DD"
      :class="{ invalid: !isStartDateValid && startDate.length > 0 }"
    />
  </label>

  <label style="margin-left: 1em;">
    End Date:
    <input
      type="text"
      v-model="endDate"
      placeholder="YYYY-MM-DD"
      :class="{ invalid: !isEndDateValid && endDate.length > 0 }"
    />
  </label>
</template>

<style scoped>
.invalid {
  border-color: red;
  outline: none;
}
</style>
