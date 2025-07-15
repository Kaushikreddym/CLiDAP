<template>
  <div ref="mapContainer" style="height: 400px; width: 100%; border: 1px solid #ccc"></div>
  <div class="mt-4">
    <p><strong>Selected Bounds:</strong></p>
    <p>South: {{ bounds[0][1].toFixed(4) }}, West: {{ bounds[0][0].toFixed(4) }}</p>
    <p>North: {{ bounds[1][1].toFixed(4) }}, East: {{ bounds[1][0].toFixed(4) }}</p>
  </div>
</template>

<script setup>
import { ref, onMounted, onBeforeUnmount, watch, defineEmits } from 'vue'
import Map from 'ol/Map'
import View from 'ol/View'
import TileLayer from 'ol/layer/Tile'
import VectorLayer from 'ol/layer/Vector'
import VectorSource from 'ol/source/Vector'
import OSM from 'ol/source/OSM'
import { fromLonLat, toLonLat } from 'ol/proj'
import Feature from 'ol/Feature'
import Polygon from 'ol/geom/Polygon'
import { Style, Stroke, Fill } from 'ol/style'
import DragBox from 'ol/interaction/DragBox'
import { platformModifierKeyOnly } from 'ol/events/condition'

const emits = defineEmits(['update:bounds'])

const mapContainer = ref(null)
let map = null
let vectorLayer = null
let dragBox = null

const bounds = ref([
  [9.5, 50.5], // west,south
  [11.5, 52.5] // east,north
])

function createRectangleFeature(bounds) {
  const [west, south] = bounds[0]
  const [east, north] = bounds[1]
  const coords = [
    [west, south],
    [west, north],
    [east, north],
    [east, south],
    [west, south],
  ].map(coord => fromLonLat(coord))
  return new Feature(new Polygon([coords]))
}

function updateVectorLayer(bounds) {
  const feature = createRectangleFeature(bounds)
  vectorLayer.getSource().clear()
  vectorLayer.getSource().addFeature(feature)
}

function extentToBounds(extent) {
  const bottomLeft = toLonLat([extent[0], extent[1]])
  const topRight = toLonLat([extent[2], extent[3]])
  return [bottomLeft, topRight]
}

onMounted(() => {
  map = new Map({
    target: mapContainer.value,
    layers: [new TileLayer({ source: new OSM() })],
    view: new View({
      center: fromLonLat([10.4515, 51.1657]),
      zoom: 5,
    }),
  })

  vectorLayer = new VectorLayer({
    source: new VectorSource(),
    style: new Style({
      stroke: new Stroke({ color: 'blue', width: 2 }),
      fill: new Fill({ color: 'rgba(0, 0, 255, 0.1)' }),
    }),
  })

  map.addLayer(vectorLayer)
  updateVectorLayer(bounds.value)

  dragBox = new DragBox({
    condition: platformModifierKeyOnly,
  })

  map.addInteraction(dragBox)

  dragBox.on('boxend', () => {
    const extent = dragBox.getGeometry().getExtent()
    const newBounds = extentToBounds(extent)
    bounds.value = newBounds
    updateVectorLayer(newBounds)
    emits('update:bounds', newBounds)
  })

  dragBox.on('boxstart', () => {
    vectorLayer.getSource().clear()
  })
})

onBeforeUnmount(() => {
  if (map) {
    map.setTarget(null)
  }
})
</script>
