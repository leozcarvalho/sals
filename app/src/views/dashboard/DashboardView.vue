<script setup>
import { ref, onMounted } from "vue";
import TemplateSVG from "./TemplateSVG.vue";
</script>

<template>
  <BaseBackground>
    <div class="content content-full text-center">
      <!-- Container com rolagem lateral -->
      <div class="overflow-auto" style="white-space: nowrap;">
        <TemplateSVG />
      </div>
    </div>
  </BaseBackground>
</template>

<style scoped>
.overflow-auto {
  overflow-x: auto;
  overflow-y: hidden;
  padding-bottom: 10px;
}

/* Barra de rolagem discreta */
.overflow-auto::-webkit-scrollbar {
  height: 8px;
}
.overflow-auto::-webkit-scrollbar-thumb {
  background: #bbb;
  border-radius: 4px;
}
.overflow-auto::-webkit-scrollbar-thumb:hover {
  background: #999;
}
</style>