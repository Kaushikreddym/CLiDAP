<template><div id="webcrumbs"><div class="bg-gradient-to-b from-blue-50 to-green-50 min-h-screen p-4 md:p-6 lg:p-8">  <header class="bg-white rounded-xl shadow-md p-4 mb-6 flex flex-col md:flex-row justify-between items-center"> <div class="flex items-center mb-4 md:mb-0"> <span class="text-3xl text-primary-600 mr-3 material-symbols-outlined">home</span> <h1 class="text-2xl font-bold text-gray-800">CLImate Data Access Dashboard</h1> </div> <div class="flex items-center space-x-4"> <button class="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg transition-all transform hover:scale-105 flex items-center"> <span class="material-symbols-outlined mr-1">download</span> Export Data </button> <button class="bg-white border border-gray-300 hover:border-primary-400 text-gray-700 px-4 py-2 rounded-lg transition-all transform hover:scale-105 flex items-center"> <span class="material-symbols-outlined mr-1">settings</span> Settings </button> </div> </header>  <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-6">  <div class="bg-white rounded-xl shadow-md p-4 lg:col-span-2 hover:shadow-lg transition-shadow"> <div class="flex justify-between items-center mb-4"> <h2 class="text-xl font-semibold text-gray-800">Global Temperature Anomalies</h2> <div class="flex space-x-2"> <button class="p-2 rounded-full hover:bg-gray-100 transition-colors"> <span class="material-symbols-outlined text-gray-600">download</span> </button> <button class="p-2 rounded-full hover:bg-gray-100 transition-colors"> <span class="material-symbols-outlined text-gray-600">more_vert</span> </button> </div> </div> <div class="h-[300px] relative"> <div data-chart="chart_0"></div> </div> </div>  <div class="bg-white rounded-xl shadow-md p-4 hover:shadow-lg transition-shadow"> <div class="flex justify-between items-center mb-4"> <h2 class="text-xl font-semibold text-gray-800">CO2 Concentration</h2> <div class="flex space-x-2"> <button class="p-2 rounded-full hover:bg-gray-100 transition-colors"> <span class="material-symbols-outlined text-gray-600">download</span> </button> </div> </div> <div class="h-[300px] relative"> <div data-chart="chart_1"></div> </div> </div>  <div class="bg-white rounded-xl shadow-md p-4 hover:shadow-lg transition-shadow"> <div class="flex justify-between items-center mb-4"> <h2 class="text-xl font-semibold text-gray-800">Sea Level Rise</h2> <div class="flex space-x-2"> <button class="p-2 rounded-full hover:bg-gray-100 transition-colors"> <span class="material-symbols-outlined text-gray-600">download</span> </button> </div> </div> <div class="h-[300px] relative"> <div data-chart="chart_2"></div> </div> </div>  <div class="bg-white rounded-xl shadow-md p-4 hover:shadow-lg transition-shadow"> <div class="flex justify-between items-center mb-4"> <h2 class="text-xl font-semibold text-gray-800">Arctic Sea Ice Extent</h2> <div class="flex space-x-2"> <button class="p-2 rounded-full hover:bg-gray-100 transition-colors"> <span class="material-symbols-outlined text-gray-600">download</span> </button> </div> </div> <div class="h-[300px] relative"> <div data-chart="chart_3"></div> </div> </div>  <div class="bg-white rounded-xl shadow-md p-4 hover:shadow-lg transition-shadow lg:col-span-2"> <h2 class="text-xl font-semibold text-gray-800 mb-4">Data Sources</h2> <div class="space-y-4"> <details class="group"> <summary class="flex justify-between items-center cursor-pointer p-3 rounded-lg hover:bg-gray-50 transition-colors"> <div class="flex items-center"> <span class="material-symbols-outlined text-primary-500 mr-2">dataset</span> <span class="font-medium">NASA GISS Temperature Data</span> </div> <span class="material-symbols-outlined transform group-open:rotate-180 transition-transform">expand_more</span> </summary> <div class="p-3 bg-gray-50 rounded-lg mt-2"> <p class="text-gray-600">Global surface temperature data from NASA&#x27;s Goddard Institute for Space Studies. Provides monthly and annual temperature anomalies relative to a base period.</p> <div class="flex mt-3"> <button class="text-primary-600 hover:text-primary-700 flex items-center transition-colors"> <span class="material-symbols-outlined mr-1 text-sm">download</span> Download CSV </button> <button class="text-primary-600 hover:text-primary-700 flex items-center ml-4 transition-colors"> <span class="material-symbols-outlined mr-1 text-sm">open_in_new</span> Visit Source </button> </div> </div> </details> <details class="group"> <summary class="flex justify-between items-center cursor-pointer p-3 rounded-lg hover:bg-gray-50 transition-colors"> <div class="flex items-center"> <span class="material-symbols-outlined text-primary-500 mr-2">co2</span> <span class="font-medium">NOAA CO2 Measurements</span> </div> <span class="material-symbols-outlined transform group-open:rotate-180 transition-transform">expand_more</span> </summary> <div class="p-3 bg-gray-50 rounded-lg mt-2"> <p class="text-gray-600">Atmospheric CO2 concentration data from NOAA&#x27;s Mauna Loa Observatory. Includes daily, monthly and annual average CO2 measurements.</p> <div class="flex mt-3"> <button class="text-primary-600 hover:text-primary-700 flex items-center transition-colors"> <span class="material-symbols-outlined mr-1 text-sm">download</span> Download CSV </button> <button class="text-primary-600 hover:text-primary-700 flex items-center ml-4 transition-colors"> <span class="material-symbols-outlined mr-1 text-sm">open_in_new</span> Visit Source </button> </div> </div> </details> <details class="group"> <summary class="flex justify-between items-center cursor-pointer p-3 rounded-lg hover:bg-gray-50 transition-colors"> <div class="flex items-center"> <span class="material-symbols-outlined text-primary-500 mr-2">water</span> <span class="font-medium">Sea Level and Ice Data</span> </div> <span class="material-symbols-outlined transform group-open:rotate-180 transition-transform">expand_more</span> </summary> <div class="p-3 bg-gray-50 rounded-lg mt-2"> <p class="text-gray-600">Sea level data from satellite altimetry and Arctic sea ice extent measurements from the National Snow and Ice Data Center (NSIDC).</p> <div class="flex mt-3"> <button class="text-primary-600 hover:text-primary-700 flex items-center transition-colors"> <span class="material-symbols-outlined mr-1 text-sm">download</span> Download CSV </button> <button class="text-primary-600 hover:text-primary-700 flex items-center ml-4 transition-colors"> <span class="material-symbols-outlined mr-1 text-sm">open_in_new</span> Visit Source </button> </div> </div> </details> </div> </div> </div><div class="bg-white rounded-xl shadow-md p-6 mb-6 hover:shadow-lg transition-shadow"> <h2 class="text-xl font-semibold text-gray-800 mb-4 flex items-center"> <span class="material-symbols-outlined text-primary-500 mr-2">filter_alt</span> Advanced Data Filtering </h2> <div class="grid grid-cols-1 md:grid-cols-3 gap-6"> <div class="space-y-4"> <div> <label class="block text-sm font-medium text-gray-700 mb-1">Date Range</label> <div class="flex items-center space-x-2"> <input type="date" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-300 focus:border-primary-500 transition-all" placeholder="From"/> <span class="text-gray-500">to</span> <input type="date" class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-300 focus:border-primary-500 transition-all" placeholder="To"/> </div> </div> <div> <label class="block text-sm font-medium text-gray-700 mb-1">Data Source</label> <select class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-300 focus:border-primary-500 transition-all"> <option>All Sources</option> <option>NASA GISS Temperature Data</option> <option>NOAA CO2 Measurements</option> <option>Sea Level Data</option> <option>Arctic Ice Data</option> </select> </div> </div> <div class="space-y-4"> <div> <label class="block text-sm font-medium text-gray-700 mb-1">Data Resolution</label> <div class="flex items-center space-x-3"> <label class="inline-flex items-center"> <input type="radio" name="resolution" class="h-4 w-4 text-primary-600 focus:ring-primary-500"/> <span class="ml-2 text-sm text-gray-700">Daily</span> </label> <label class="inline-flex items-center"> <input type="radio" name="resolution" class="h-4 w-4 text-primary-600 focus:ring-primary-500" checked=""/> <span class="ml-2 text-sm text-gray-700">Monthly</span> </label> <label class="inline-flex items-center"> <input type="radio" name="resolution" class="h-4 w-4 text-primary-600 focus:ring-primary-500"/> <span class="ml-2 text-sm text-gray-700">Annual</span> </label> </div> </div> <div> <label class="block text-sm font-medium text-gray-700 mb-1">Geographic Region</label> <select class="w-full px-3 py-2 border border-gray-300 rounded-lg focus:ring-2 focus:ring-primary-300 focus:border-primary-500 transition-all"> <option>Global</option> <option>Northern Hemisphere</option> <option>Southern Hemisphere</option> <option>Tropics</option> <option>Arctic</option> <option>Antarctic</option> </select> </div> </div> <div class="space-y-4"> <div> <label class="block text-sm font-medium text-gray-700 mb-1">Advanced Filters</label> <div class="space-y-2"> <label class="inline-flex items-center"> <input type="checkbox" class="h-4 w-4 text-primary-600 focus:ring-primary-500"/> <span class="ml-2 text-sm text-gray-700">Seasonal Adjustment</span> </label> <label class="inline-flex items-center"> <input type="checkbox" class="h-4 w-4 text-primary-600 focus:ring-primary-500"/> <span class="ml-2 text-sm text-gray-700">Remove Outliers</span> </label> <label class="inline-flex items-center"> <input type="checkbox" class="h-4 w-4 text-primary-600 focus:ring-primary-500"/> <span class="ml-2 text-sm text-gray-700">Show Trend Lines</span> </label> </div> </div> <div class="flex space-x-3 mt-8"> <button class="bg-primary-500 hover:bg-primary-600 text-white px-4 py-2 rounded-lg transition-all transform hover:scale-105 flex-1 flex items-center justify-center"> <span class="material-symbols-outlined mr-1">search</span> Apply Filters </button> <button class="bg-white border border-gray-300 hover:border-gray-400 text-gray-700 px-3 py-2 rounded-lg transition-all flex items-center justify-center"> <span class="material-symbols-outlined">restart_alt</span> </button> </div> </div> </div> <div class="mt-4 pt-4 border-t border-gray-100"> <div class="flex items-center justify-between"> <div class="text-sm text-gray-500"> <span class="font-medium">Active filters:</span> Monthly data, Global region, 2013-2022 </div> <div class="flex items-center"> <button class="text-primary-600 hover:text-primary-700 text-sm flex items-center transition-colors"> <span class="material-symbols-outlined mr-1 text-sm">save</span> Save Filter Set </button> <span class="mx-2 text-gray-300">|</span> <button class="text-primary-600 hover:text-primary-700 text-sm flex items-center transition-colors"> <span class="material-symbols-outlined mr-1 text-sm">share</span> Share Filtered View </button> </div> </div> </div> </div>  <div class="mt-6 bg-white rounded-xl shadow-md p-4"> <h2 class="text-xl font-semibold text-gray-800 mb-4">Data Analysis Tools</h2> <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-4 gap-4"> <div class="border border-gray-200 rounded-lg p-4 hover:border-primary-300 hover:shadow-md transition-all transform hover:scale-[1.02]"> <div class="flex items-center mb-2"> <span class="material-symbols-outlined text-primary-500 mr-2">show_chart</span> <h3 class="font-medium">Custom Plotting</h3> </div> <p class="text-gray-600 text-sm mb-3">Create customized plots with multiple variables and timeframes.</p> <button class="w-full bg-primary-50 hover:bg-primary-100 text-primary-700 py-2 rounded-lg transition-colors"> Open Plotter </button> </div> <div class="border border-gray-200 rounded-lg p-4 hover:border-primary-300 hover:shadow-md transition-all transform hover:scale-[1.02]"> <div class="flex items-center mb-2"> <span class="material-symbols-outlined text-primary-500 mr-2">calculate</span> <h3 class="font-medium">Statistical Analysis</h3> </div> <p class="text-gray-600 text-sm mb-3">Perform statistical tests and calculate trends in climate data.</p> <button class="w-full bg-primary-50 hover:bg-primary-100 text-primary-700 py-2 rounded-lg transition-colors"> Run Analysis </button> </div> <div class="border border-gray-200 rounded-lg p-4 hover:border-primary-300 hover:shadow-md transition-all transform hover:scale-[1.02]"> <div class="flex items-center mb-2"> <span class="material-symbols-outlined text-primary-500 mr-2">compare_arrows</span> <h3 class="font-medium">Data Comparison</h3> </div> <p class="text-gray-600 text-sm mb-3">Compare different climate indicators and discover correlations.</p> <button class="w-full bg-primary-50 hover:bg-primary-100 text-primary-700 py-2 rounded-lg transition-colors"> Compare Data </button> </div> <div class="border border-gray-200 rounded-lg p-4 hover:border-primary-300 hover:shadow-md transition-all transform hover:scale-[1.02]"> <div class="flex items-center mb-2"> <span class="material-symbols-outlined text-primary-500 mr-2">download</span> <h3 class="font-medium">Bulk Download</h3> </div> <p class="text-gray-600 text-sm mb-3">Download multiple datasets in various formats (CSV, JSON, Excel).</p> <button class="w-full bg-primary-50 hover:bg-primary-100 text-primary-700 py-2 rounded-lg transition-colors"> Download Center </button> </div> </div>  </div>  <footer class="mt-8 text-center text-gray-500 text-sm"> <p>ClimateViz Dashboard © 2023 | Data updated daily from official sources</p> <div class="flex justify-center mt-2 space-x-4"> <a href="#" class="hover:text-primary-500 transition-colors">Terms</a> <a href="#" class="hover:text-primary-500 transition-colors">Privacy</a> <a href="#" class="hover:text-primary-500 transition-colors">Data Usage</a> <a href="#" class="hover:text-primary-500 transition-colors">Contact</a> </div>  </footer> </div></div></template>

<style scoped>
@import url(https://fonts.googleapis.com/css2?family=Lato&display=swap);
@import url(https://fonts.googleapis.com/css2?family=Open+Sans&display=swap);
@import url(https://fonts.googleapis.com/css2?family=Material+Symbols+Outlined);

*,
:after,
:before {
  --tw-border-spacing-x: 0;
  --tw-border-spacing-y: 0;
  --tw-translate-x: 0;
  --tw-translate-y: 0;
  --tw-rotate: 0;
  --tw-skew-x: 0;
  --tw-skew-y: 0;
  --tw-scale-x: 1;
  --tw-scale-y: 1;
  --tw-pan-x: ;
  --tw-pan-y: ;
  --tw-pinch-zoom: ;
  --tw-scroll-snap-strictness: proximity;
  --tw-gradient-from-position: ;
  --tw-gradient-via-position: ;
  --tw-gradient-to-position: ;
  --tw-ordinal: ;
  --tw-slashed-zero: ;
  --tw-numeric-figure: ;
  --tw-numeric-spacing: ;
  --tw-numeric-fraction: ;
  --tw-ring-inset: ;
  --tw-ring-offset-width: 0px;
  --tw-ring-offset-color: #fff;
  --tw-ring-color: rgba(59, 130, 246, 0.5);
  --tw-ring-offset-shadow: 0 0 #0000;
  --tw-ring-shadow: 0 0 #0000;
  --tw-shadow: 0 0 #0000;
  --tw-shadow-colored: 0 0 #0000;
  --tw-blur: ;
  --tw-brightness: ;
  --tw-contrast: ;
  --tw-grayscale: ;
  --tw-hue-rotate: ;
  --tw-invert: ;
  --tw-saturate: ;
  --tw-sepia: ;
  --tw-drop-shadow: ;
  --tw-backdrop-blur: ;
  --tw-backdrop-brightness: ;
  --tw-backdrop-contrast: ;
  --tw-backdrop-grayscale: ;
  --tw-backdrop-hue-rotate: ;
  --tw-backdrop-invert: ;
  --tw-backdrop-opacity: ;
  --tw-backdrop-saturate: ;
  --tw-backdrop-sepia: ;
  --tw-contain-size: ;
  --tw-contain-layout: ;
  --tw-contain-paint: ;
  --tw-contain-style: ;
}
::backdrop {
  --tw-border-spacing-x: 0;
  --tw-border-spacing-y: 0;
  --tw-translate-x: 0;
  --tw-translate-y: 0;
  --tw-rotate: 0;
  --tw-skew-x: 0;
  --tw-skew-y: 0;
  --tw-scale-x: 1;
  --tw-scale-y: 1;
  --tw-pan-x: ;
  --tw-pan-y: ;
  --tw-pinch-zoom: ;
  --tw-scroll-snap-strictness: proximity;
  --tw-gradient-from-position: ;
  --tw-gradient-via-position: ;
  --tw-gradient-to-position: ;
  --tw-ordinal: ;
  --tw-slashed-zero: ;
  --tw-numeric-figure: ;
  --tw-numeric-spacing: ;
  --tw-numeric-fraction: ;
  --tw-ring-inset: ;
  --tw-ring-offset-width: 0px;
  --tw-ring-offset-color: #fff;
  --tw-ring-color: rgba(59, 130, 246, 0.5);
  --tw-ring-offset-shadow: 0 0 #0000;
  --tw-ring-shadow: 0 0 #0000;
  --tw-shadow: 0 0 #0000;
  --tw-shadow-colored: 0 0 #0000;
  --tw-blur: ;
  --tw-brightness: ;
  --tw-contrast: ;
  --tw-grayscale: ;
  --tw-hue-rotate: ;
  --tw-invert: ;
  --tw-saturate: ;
  --tw-sepia: ;
  --tw-drop-shadow: ;
  --tw-backdrop-blur: ;
  --tw-backdrop-brightness: ;
  --tw-backdrop-contrast: ;
  --tw-backdrop-grayscale: ;
  --tw-backdrop-hue-rotate: ;
  --tw-backdrop-invert: ;
  --tw-backdrop-opacity: ;
  --tw-backdrop-saturate: ;
  --tw-backdrop-sepia: ;
  --tw-contain-size: ;
  --tw-contain-layout: ;
  --tw-contain-paint: ;
  --tw-contain-style: ;
} /*! tailwindcss v3.4.17 | MIT License | https://tailwindcss.com*/
*,
:after,
:before {
  border: 0 solid #e5e7eb;
  box-sizing: border-box;
}
:after,
:before {
  --tw-content: "";
}
:host,
html {
  line-height: 1.5;
  -webkit-text-size-adjust: 100%;
  font-family:
    Open Sans,
    ui-sans-serif,
    system-ui,
    sans-serif,
    Apple Color Emoji,
    Segoe UI Emoji,
    Segoe UI Symbol,
    Noto Color Emoji;
  font-feature-settings: normal;
  font-variation-settings: normal;
  -moz-tab-size: 4;
  tab-size: 4;
  -webkit-tap-highlight-color: transparent;
}
body {
  line-height: inherit;
  margin: 0;
}
hr {
  border-top-width: 1px;
  color: inherit;
  height: 0;
}
abbr:where([title]) {
  text-decoration: underline dotted;
}
h1,
h2,
h3,
h4,
h5,
h6 {
  font-size: inherit;
  font-weight: inherit;
}
a {
  color: inherit;
  text-decoration: inherit;
}
b,
strong {
  font-weight: bolder;
}
code,
kbd,
pre,
samp {
  font-family:
    ui-monospace,
    SFMono-Regular,
    Menlo,
    Monaco,
    Consolas,
    Liberation Mono,
    Courier New,
    monospace;
  font-feature-settings: normal;
  font-size: 1em;
  font-variation-settings: normal;
}
small {
  font-size: 80%;
}
sub,
sup {
  font-size: 75%;
  line-height: 0;
  position: relative;
  vertical-align: baseline;
}
sub {
  bottom: -0.25em;
}
sup {
  top: -0.5em;
}
table {
  border-collapse: collapse;
  border-color: inherit;
  text-indent: 0;
}
button,
input,
optgroup,
select,
textarea {
  color: inherit;
  font-family: inherit;
  font-feature-settings: inherit;
  font-size: 100%;
  font-variation-settings: inherit;
  font-weight: inherit;
  letter-spacing: inherit;
  line-height: inherit;
  margin: 0;
  padding: 0;
}
button,
select {
  text-transform: none;
}
button,
input:where([type="button"]),
input:where([type="reset"]),
input:where([type="submit"]) {
  -webkit-appearance: button;
  background-color: transparent;
  background-image: none;
}
:-moz-focusring {
  outline: auto;
}
:-moz-ui-invalid {
  box-shadow: none;
}
progress {
  vertical-align: baseline;
}
::-webkit-inner-spin-button,
::-webkit-outer-spin-button {
  height: auto;
}
[type="search"] {
  -webkit-appearance: textfield;
  outline-offset: -2px;
}
::-webkit-search-decoration {
  -webkit-appearance: none;
}
::-webkit-file-upload-button {
  -webkit-appearance: button;
  font: inherit;
}
summary {
  display: list-item;
}
blockquote,
dd,
dl,
figure,
h1,
h2,
h3,
h4,
h5,
h6,
hr,
p,
pre {
  margin: 0;
}
fieldset {
  margin: 0;
}
fieldset,
legend {
  padding: 0;
}
menu,
ol,
ul {
  list-style: none;
  margin: 0;
  padding: 0;
}
dialog {
  padding: 0;
}
textarea {
  resize: vertical;
}
input::placeholder,
textarea::placeholder {
  color: #9ca3af;
  opacity: 1;
}
[role="button"],
button {
  cursor: pointer;
}
:disabled {
  cursor: default;
}
audio,
canvas,
embed,
iframe,
img,
object,
svg,
video {
  display: block;
  vertical-align: middle;
}
img,
video {
  height: auto;
  max-width: 100%;
}
[hidden]:where(:not([hidden="until-found"])) {
  display: none;
}
#webcrumbs .relative {
  position: relative;
}
#webcrumbs .mx-2 {
  margin-left: 8px;
  margin-right: 8px;
}
#webcrumbs .mb-1 {
  margin-bottom: 4px;
}
#webcrumbs .mb-2 {
  margin-bottom: 8px;
}
#webcrumbs .mb-3 {
  margin-bottom: 12px;
}
#webcrumbs .mb-4 {
  margin-bottom: 16px;
}
#webcrumbs .mb-6 {
  margin-bottom: 24px;
}
#webcrumbs .ml-2 {
  margin-left: 8px;
}
#webcrumbs .ml-4 {
  margin-left: 16px;
}
#webcrumbs .mr-1 {
  margin-right: 4px;
}
#webcrumbs .mr-2 {
  margin-right: 8px;
}
#webcrumbs .mr-3 {
  margin-right: 12px;
}
#webcrumbs .mt-2 {
  margin-top: 8px;
}
#webcrumbs .mt-3 {
  margin-top: 12px;
}
#webcrumbs .mt-4 {
  margin-top: 16px;
}
#webcrumbs .mt-6 {
  margin-top: 24px;
}
#webcrumbs .mt-8 {
  margin-top: 32px;
}
#webcrumbs .block {
  display: block;
}
#webcrumbs .flex {
  display: flex;
}
#webcrumbs .inline-flex {
  display: inline-flex;
}
#webcrumbs .grid {
  display: grid;
}
#webcrumbs .h-4 {
  height: 16px;
}
#webcrumbs .h-\[300px\] {
  height: 300px;
}
#webcrumbs .min-h-screen {
  min-height: 100vh;
}
#webcrumbs .w-4 {
  width: 16px;
}
#webcrumbs .w-full {
  width: 100%;
}
#webcrumbs .flex-1 {
  flex: 1 1 0%;
}
#webcrumbs .transform {
  transform: translate(var(--tw-translate-x), var(--tw-translate-y))
    rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y))
    scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y));
}
#webcrumbs .cursor-pointer {
  cursor: pointer;
}
#webcrumbs .grid-cols-1 {
  grid-template-columns: repeat(1, minmax(0, 1fr));
}
#webcrumbs .flex-row {
  flex-direction: row;
}
#webcrumbs .flex-col {
  flex-direction: column;
}
#webcrumbs .items-center {
  align-items: center;
}
#webcrumbs .justify-center {
  justify-content: center;
}
#webcrumbs .justify-between {
  justify-content: space-between;
}
#webcrumbs .gap-4 {
  gap: 16px;
}
#webcrumbs .gap-6 {
  gap: 24px;
}
#webcrumbs :is(.space-x-2 > :not([hidden]) ~ :not([hidden])) {
  --tw-space-x-reverse: 0;
  margin-left: calc(8px * (1 - var(--tw-space-x-reverse)));
  margin-right: calc(8px * var(--tw-space-x-reverse));
}
#webcrumbs :is(.space-x-3 > :not([hidden]) ~ :not([hidden])) {
  --tw-space-x-reverse: 0;
  margin-left: calc(12px * (1 - var(--tw-space-x-reverse)));
  margin-right: calc(12px * var(--tw-space-x-reverse));
}
#webcrumbs :is(.space-x-4 > :not([hidden]) ~ :not([hidden])) {
  --tw-space-x-reverse: 0;
  margin-left: calc(16px * (1 - var(--tw-space-x-reverse)));
  margin-right: calc(16px * var(--tw-space-x-reverse));
}
#webcrumbs :is(.space-y-2 > :not([hidden]) ~ :not([hidden])) {
  --tw-space-y-reverse: 0;
  margin-bottom: calc(8px * var(--tw-space-y-reverse));
  margin-top: calc(8px * (1 - var(--tw-space-y-reverse)));
}
#webcrumbs :is(.space-y-4 > :not([hidden]) ~ :not([hidden])) {
  --tw-space-y-reverse: 0;
  margin-bottom: calc(16px * var(--tw-space-y-reverse));
  margin-top: calc(16px * (1 - var(--tw-space-y-reverse)));
}
#webcrumbs .rounded-full {
  border-radius: 9999px;
}
#webcrumbs .rounded-lg {
  border-radius: 24px;
}
#webcrumbs .rounded-xl {
  border-radius: 36px;
}
#webcrumbs .border {
  border-width: 1px;
}
#webcrumbs .border-t {
  border-top-width: 1px;
}
#webcrumbs .border-gray-100 {
  --tw-border-opacity: 1;
  border-color: rgb(243 244 246 / var(--tw-border-opacity, 1));
}
#webcrumbs .border-gray-200 {
  --tw-border-opacity: 1;
  border-color: rgb(229 231 235 / var(--tw-border-opacity, 1));
}
#webcrumbs .border-gray-300 {
  --tw-border-opacity: 1;
  border-color: rgb(209 213 219 / var(--tw-border-opacity, 1));
}
#webcrumbs .bg-gray-50 {
  --tw-bg-opacity: 1;
  background-color: rgb(249 250 251 / var(--tw-bg-opacity, 1));
}
#webcrumbs .bg-primary-50 {
  --tw-bg-opacity: 1;
  background-color: rgb(243 241 255 / var(--tw-bg-opacity, 1));
}
#webcrumbs .bg-primary-500 {
  --tw-bg-opacity: 1;
  background-color: rgb(115 65 255 / var(--tw-bg-opacity, 1));
}
#webcrumbs .bg-white {
  --tw-bg-opacity: 1;
  background-color: rgb(255 255 255 / var(--tw-bg-opacity, 1));
}
#webcrumbs .bg-gradient-to-b {
  background-image: linear-gradient(to bottom, var(--tw-gradient-stops));
}
#webcrumbs .from-blue-50 {
  --tw-gradient-from: #eff6ff var(--tw-gradient-from-position);
  --tw-gradient-to: rgba(239, 246, 255, 0) var(--tw-gradient-to-position);
  --tw-gradient-stops: var(--tw-gradient-from), var(--tw-gradient-to);
}
#webcrumbs .to-green-50 {
  --tw-gradient-to: #f0fdf4 var(--tw-gradient-to-position);
}
#webcrumbs .p-2 {
  padding: 8px;
}
#webcrumbs .p-3 {
  padding: 12px;
}
#webcrumbs .p-4 {
  padding: 16px;
}
#webcrumbs .p-6 {
  padding: 24px;
}
#webcrumbs .px-3 {
  padding-left: 12px;
  padding-right: 12px;
}
#webcrumbs .px-4 {
  padding-left: 16px;
  padding-right: 16px;
}
#webcrumbs .py-2 {
  padding-bottom: 8px;
  padding-top: 8px;
}
#webcrumbs .pt-4 {
  padding-top: 16px;
}
#webcrumbs .text-center {
  text-align: center;
}
#webcrumbs .text-2xl {
  font-size: 24px;
  line-height: 31.200000000000003px;
}
#webcrumbs .text-3xl {
  font-size: 30px;
  line-height: 36px;
}
#webcrumbs .text-sm {
  font-size: 14px;
  line-height: 21px;
}
#webcrumbs .text-xl {
  font-size: 20px;
  line-height: 28px;
}
#webcrumbs .font-bold {
  font-weight: 700;
}
#webcrumbs .font-medium {
  font-weight: 500;
}
#webcrumbs .font-semibold {
  font-weight: 600;
}
#webcrumbs .text-gray-300 {
  --tw-text-opacity: 1;
  color: rgb(209 213 219 / var(--tw-text-opacity, 1));
}
#webcrumbs .text-gray-500 {
  --tw-text-opacity: 1;
  color: rgb(107 114 128 / var(--tw-text-opacity, 1));
}
#webcrumbs .text-gray-600 {
  --tw-text-opacity: 1;
  color: rgb(75 85 99 / var(--tw-text-opacity, 1));
}
#webcrumbs .text-gray-700 {
  --tw-text-opacity: 1;
  color: rgb(55 65 81 / var(--tw-text-opacity, 1));
}
#webcrumbs .text-gray-800 {
  --tw-text-opacity: 1;
  color: rgb(31 41 55 / var(--tw-text-opacity, 1));
}
#webcrumbs .text-primary-500 {
  --tw-text-opacity: 1;
  color: rgb(115 65 255 / var(--tw-text-opacity, 1));
}
#webcrumbs .text-primary-600 {
  --tw-text-opacity: 1;
  color: rgb(99 27 255 / var(--tw-text-opacity, 1));
}
#webcrumbs .text-primary-700 {
  --tw-text-opacity: 1;
  color: rgb(97 27 248 / var(--tw-text-opacity, 1));
}
#webcrumbs .text-white {
  --tw-text-opacity: 1;
  color: rgb(255 255 255 / var(--tw-text-opacity, 1));
}
#webcrumbs .shadow-md {
  --tw-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
  --tw-shadow-colored:
    0 4px 6px -1px var(--tw-shadow-color), 0 2px 4px -2px var(--tw-shadow-color);
  box-shadow:
    var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000),
    var(--tw-shadow);
}
#webcrumbs .transition-all {
  transition-duration: 0.15s;
  transition-property: all;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
#webcrumbs .transition-colors {
  transition-duration: 0.15s;
  transition-property:
    color, background-color, border-color, text-decoration-color, fill, stroke;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
#webcrumbs .transition-shadow {
  transition-duration: 0.15s;
  transition-property: box-shadow;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
#webcrumbs .transition-transform {
  transition-duration: 0.15s;
  transition-property: transform;
  transition-timing-function: cubic-bezier(0.4, 0, 0.2, 1);
}
#webcrumbs {
  font-family: Open Sans !important;
  font-size: 16px !important;
}
#webcrumbs :is(.bg-primary-50) {
  color: rgba(0, 0, 0, 0.9) !important;
}
#webcrumbs :is(.bg-primary-500) {
  color: hsla(0, 0%, 100%, 0.9) !important;
}
#webcrumbs .hover\:scale-105:hover {
  --tw-scale-x: 1.05;
  --tw-scale-y: 1.05;
}
#webcrumbs .hover\:scale-105:hover,
#webcrumbs .hover\:scale-\[1\.02\]:hover {
  transform: translate(var(--tw-translate-x), var(--tw-translate-y))
    rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y))
    scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y));
}
#webcrumbs .hover\:scale-\[1\.02\]:hover {
  --tw-scale-x: 1.02;
  --tw-scale-y: 1.02;
}
#webcrumbs .hover\:border-gray-400:hover {
  --tw-border-opacity: 1;
  border-color: rgb(156 163 175 / var(--tw-border-opacity, 1));
}
#webcrumbs .hover\:border-primary-300:hover {
  --tw-border-opacity: 1;
  border-color: rgb(183 169 255 / var(--tw-border-opacity, 1));
}
#webcrumbs .hover\:border-primary-400:hover {
  --tw-border-opacity: 1;
  border-color: rgb(148 120 255 / var(--tw-border-opacity, 1));
}
#webcrumbs .hover\:bg-gray-100:hover {
  --tw-bg-opacity: 1;
  background-color: rgb(243 244 246 / var(--tw-bg-opacity, 1));
}
#webcrumbs .hover\:bg-gray-50:hover {
  --tw-bg-opacity: 1;
  background-color: rgb(249 250 251 / var(--tw-bg-opacity, 1));
}
#webcrumbs .hover\:bg-primary-100:hover {
  --tw-bg-opacity: 1;
  background-color: rgb(233 229 255 / var(--tw-bg-opacity, 1));
}
#webcrumbs .hover\:bg-primary-600:hover {
  --tw-bg-opacity: 1;
  background-color: rgb(99 27 255 / var(--tw-bg-opacity, 1));
}
#webcrumbs .hover\:text-primary-500:hover {
  --tw-text-opacity: 1;
  color: rgb(115 65 255 / var(--tw-text-opacity, 1));
}
#webcrumbs .hover\:text-primary-700:hover {
  --tw-text-opacity: 1;
  color: rgb(97 27 248 / var(--tw-text-opacity, 1));
}
#webcrumbs .hover\:shadow-lg:hover {
  --tw-shadow:
    0 10px 15px -3px rgba(0, 0, 0, 0.1), 0 4px 6px -4px rgba(0, 0, 0, 0.1);
  --tw-shadow-colored:
    0 10px 15px -3px var(--tw-shadow-color),
    0 4px 6px -4px var(--tw-shadow-color);
}
#webcrumbs .hover\:shadow-lg:hover,
#webcrumbs .hover\:shadow-md:hover {
  box-shadow:
    var(--tw-ring-offset-shadow, 0 0 #0000), var(--tw-ring-shadow, 0 0 #0000),
    var(--tw-shadow);
}
#webcrumbs .hover\:shadow-md:hover {
  --tw-shadow:
    0 4px 6px -1px rgba(0, 0, 0, 0.1), 0 2px 4px -2px rgba(0, 0, 0, 0.1);
  --tw-shadow-colored:
    0 4px 6px -1px var(--tw-shadow-color), 0 2px 4px -2px var(--tw-shadow-color);
}
#webcrumbs .focus\:border-primary-500:focus {
  --tw-border-opacity: 1;
  border-color: rgb(115 65 255 / var(--tw-border-opacity, 1));
}
#webcrumbs .focus\:ring-2:focus {
  --tw-ring-offset-shadow: var(--tw-ring-inset) 0 0 0
    var(--tw-ring-offset-width) var(--tw-ring-offset-color);
  --tw-ring-shadow: var(--tw-ring-inset) 0 0 0
    calc(2px + var(--tw-ring-offset-width)) var(--tw-ring-color);
  box-shadow:
    var(--tw-ring-offset-shadow), var(--tw-ring-shadow),
    var(--tw-shadow, 0 0 #0000);
}
#webcrumbs .focus\:ring-primary-300:focus {
  --tw-ring-opacity: 1;
  --tw-ring-color: rgb(183 169 255 / var(--tw-ring-opacity, 1));
}
#webcrumbs .focus\:ring-primary-500:focus {
  --tw-ring-opacity: 1;
  --tw-ring-color: rgb(115 65 255 / var(--tw-ring-opacity, 1));
}
#webcrumbs :is(.group[open] .group-open\:rotate-180) {
  --tw-rotate: 180deg;
  transform: translate(var(--tw-translate-x), var(--tw-translate-y))
    rotate(var(--tw-rotate)) skewX(var(--tw-skew-x)) skewY(var(--tw-skew-y))
    scaleX(var(--tw-scale-x)) scaleY(var(--tw-scale-y));
}
@media (min-width: 768px) {
  #webcrumbs .md\:mb-0 {
    margin-bottom: 0;
  }
  #webcrumbs .md\:grid-cols-2 {
    grid-template-columns: repeat(2, minmax(0, 1fr));
  }
  #webcrumbs .md\:grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  #webcrumbs .md\:flex-row {
    flex-direction: row;
  }
  #webcrumbs .md\:p-6 {
    padding: 24px;
  }
}
@media (min-width: 1024px) {
  #webcrumbs .lg\:col-span-2 {
    grid-column: span 2 / span 2;
  }
  #webcrumbs .lg\:grid-cols-3 {
    grid-template-columns: repeat(3, minmax(0, 1fr));
  }
  #webcrumbs .lg\:grid-cols-4 {
    grid-template-columns: repeat(4, minmax(0, 1fr));
  }
  #webcrumbs .lg\:p-8 {
    padding: 32px;
  }
}

</style>