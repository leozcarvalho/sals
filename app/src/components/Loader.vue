<script setup>
import { ref, defineExpose } from "vue";

import Loading from 'vue-loading-overlay';
import 'vue-loading-overlay/dist/css/index.css';

const loading = ref(false)
const loaderOn = () => loading.value = true
const loaderOff = () => loading.value = false

defineExpose({
  loaderOn,
  loaderOff
})
</script>

<template>
  <Loading :active="loading" />
</template>

