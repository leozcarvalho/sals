<script setup>
import { ref, onMounted, watch } from "vue";

const props = defineProps({
  // svg string content (preferred)
  svg: { type: String, default: "" },

  // optional url to fetch svg from
  src: { type: String, default: "" },

  // auto-fetch from `src` on mount if `svg` not provided
  autoFetch: { type: Boolean, default: true },

  // scale applied to rendered svg
  scale: { type: Number, default: 1 },
});

const svgContainer = ref(null);
const isDragging = ref(false);
const start = ref({ x: 0, y: 0 });
const scroll = ref({ left: 0, top: 0 });

const svgContent = ref(props.svg || "");

watch(() => props.svg, (v) => {
  svgContent.value = v || "";
});

// if src changes, try to fetch it
watch(
  () => props.src,
  async (v) => {
    if (v) await loadFromSrc(v);
  },
  { immediate: true }
);

async function loadFromSrc(url) {
  try {
    const res = await fetch(url);
    if (!res.ok) throw new Error("fetch failed");
    const text = await res.text();
    svgContent.value = text;
  } catch (err) {
    console.error("Erro ao carregar SVG:", err);
  }
}

onMounted(async () => {
  if (!svgContent.value && props.autoFetch && props.src) {
    await loadFromSrc(props.src);
  }
});

const startDrag = (e) => {
  if (!svgContainer.value) return;
  isDragging.value = true;
  svgContainer.value.style.cursor = "grabbing";
  start.value = { x: e.clientX, y: e.clientY };
  scroll.value = {
    left: svgContainer.value.scrollLeft,
    top: svgContainer.value.scrollTop,
  };
  try {
    svgContainer.value.setPointerCapture(e.pointerId);
  } catch {}
};

const onDrag = (e) => {
  if (!isDragging.value || !svgContainer.value) return;
  const dx = e.clientX - start.value.x;
  const dy = e.clientY - start.value.y;
  svgContainer.value.scrollLeft = scroll.value.left - dx;
  svgContainer.value.scrollTop = scroll.value.top - dy;
};

const endDrag = (e) => {
  if (!isDragging.value || !svgContainer.value) return;
  isDragging.value = false;
  svgContainer.value.style.cursor = "grab";
  try {
    svgContainer.value.releasePointerCapture(e.pointerId);
  } catch {}
};
</script>

<template>
  <div
    ref="svgContainer"
    class="svg-wrapper"
    @pointerdown="startDrag"
    @pointermove="onDrag"
    @pointerup="endDrag"
    @pointerleave="endDrag"
  >
    <div
      id="uploaded-svg"
      class="svg-inner"
      v-html="svgContent"
      :style="{ transform: `scale(${scale})`, transformOrigin: '0 0' }"
    />
  </div>
</template>

<style scoped>
.svg-wrapper {
  width: 100%;
  height: 100vh;
  overflow: auto;
  scrollbar-width: none;
  -ms-overflow-style: none;
  cursor: grab;
}

.svg-wrapper::-webkit-scrollbar {
  display: none;
}

.svg-inner {
  display: inline-block;
  /* allow pointer events inside the rendered SVG */
  pointer-events: auto;
}

/* if the injected svg contains its own <svg>, make it responsive / preserve layout */
.svg-inner svg {
  display: block;
  max-width: none;
  height: auto;
}
</style>