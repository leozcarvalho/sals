<script setup>
import { computed } from 'vue';

const props = defineProps({
  mediaUrl: {
    type: String,
    required: true,
  },
  customClass: {
    type: String,
    default: '', // Permite que o pai injete classes adicionais
  },
});
const getFileName = (url) => {
  return url.split("?")[0]; // Remove os parâmetros de consulta
};

const isImage = computed(() => {
  return getFileName(props.mediaUrl).match(/\.(jpeg|jpg|gif|png|webp)$/i);
});

const isVideo = computed(() => {
  return getFileName(props.mediaUrl).match(/\.(mp4|webm|ogg)$/i);
});
</script>

<template>
  <div :class="['media-preview', customClass]" v-if="isImage">
    <img :src="mediaUrl" alt="Media Preview" />
  </div>
  <div :class="['media-preview', customClass]" v-else-if="isVideo">
    <video controls :src="mediaUrl"></video>
  </div>
  <div :class="['media-preview', customClass]" v-else>
    <p>Formato de mídia não suportado.</p>
  </div>
</template>

<style scoped>
.media-preview img,
.media-preview video {
  max-width: 100%;
  height: auto;
}
</style>
