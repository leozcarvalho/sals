<script setup>
import { ref, onMounted, watch, nextTick, defineExpose } from "vue";

const props = defineProps({
  svg: { type: String, default: "" },
  src: { type: String, default: "" },
  autoFetch: { type: Boolean, default: true },
  scale: { type: Number, default: 1 },
  minScale: { type: Number, default: 0.5 },
  maxScale: { type: Number, default: 3 },
});

const svgContainer = ref(null);
const svgContent = ref(props.svg || "");
const isDragging = ref(false);
const start = ref({ x: 0, y: 0 });
const scroll = ref({ left: 0, top: 0 });
const scale = ref(props.scale);

watch(() => props.svg, (v) => (svgContent.value = v || ""));
watch(
  () => props.src,
  async (v) => {
    if (v) await loadFromSrc(v);
  },
  { immediate: true }
);

watch(
  () => props.svg,
  async (newVal) => {
    svgContent.value = newVal || "";
    await nextTick();
    injectSvg();
  },
  { immediate: true }
);

const injectSvg = () => {
  const container = svgContainer.value?.querySelector(".svg-inner");
  if (!container || !svgContent.value) return;
  container.innerHTML = svgContent.value;

  const svgEl = container.querySelector("svg");
  if (svgEl) {
    svgEl.id = "uploaded-svg";
    svgEl.style.height = "auto";
  }
}

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
  } else {
    injectSvg();
  }
});

let lastTouchDist = null;
let lastTouchCenter = null;

const getTouchDistance = (touches) => {
  const [t1, t2] = touches;
  return Math.hypot(t2.clientX - t1.clientX, t2.clientY - t1.clientY);
};

const getTouchCenter = (touches) => {
  const [t1, t2] = touches;
  return {
    x: (t1.clientX + t2.clientX) / 2,
    y: (t1.clientY + t2.clientY) / 2,
  };
};

const startDrag = (e) => {
  if (!svgContainer.value) return;
  if (e.touches && e.touches.length === 2) {
    // Pinch start
    lastTouchDist = getTouchDistance(e.touches);
    lastTouchCenter = getTouchCenter(e.touches);
    return;
  }
  const point = e.touches ? e.touches[0] : e;
  isDragging.value = true;
  start.value = { x: point.clientX, y: point.clientY };
  scroll.value = {
    left: svgContainer.value.scrollLeft,
    top: svgContainer.value.scrollTop,
  };
};

const onDrag = (e) => {
  if (!svgContainer.value) return;

  // Pinch zoom
  if (e.touches && e.touches.length === 2) {
    const dist = getTouchDistance(e.touches);
    const center = getTouchCenter(e.touches);
    if (lastTouchDist) {
      const diff = dist / lastTouchDist;
      scale.value = Math.min(
        props.maxScale,
        Math.max(props.minScale, scale.value * diff)
      );
    }
    lastTouchDist = dist;
    lastTouchCenter = center;
    return;
  }

  // Pan
  if (!isDragging.value) return;
  const point = e.touches ? e.touches[0] : e;
  const dx = point.clientX - start.value.x;
  const dy = point.clientY - start.value.y;
  svgContainer.value.scrollLeft = scroll.value.left - dx;
  svgContainer.value.scrollTop = scroll.value.top - dy;
};

const endDrag = (e) => {
  isDragging.value = false;
  lastTouchDist = null;
  lastTouchCenter = null;
};

const onDoubleTap = (() => {
  let lastTap = 0;
  return () => {
    const now = Date.now();
    if (now - lastTap < 300) {
      // double tap detected
      scale.value = props.scale; // reset zoom
    }
    lastTap = now;
  };
})();
</script>

<template>
  <div
    ref="svgContainer"
    class="svg-wrapper"
    @mousedown="startDrag"
    @mousemove="onDrag"
    @mouseup="endDrag"
    @mouseleave="endDrag"
    @touchstart.passive="startDrag"
    @touchmove.passive="onDrag"
    @touchend.passive="endDrag"
    @touchcancel.passive="endDrag"
    @click="onDoubleTap"
  >
    <div
      id="uploaded-svg"
      class="svg-inner"
      :style="{
        transform: `scale(${scale})`,
        transformOrigin: '0 0',
      }"
    />
  </div>
</template>

<style scoped>
.svg-wrapper {
  overflow: auto;
  touch-action: none; /* necessário para gestos customizados */
  -webkit-overflow-scrolling: touch;
  scrollbar-width: none;
  -ms-overflow-style: none;
}

.svg-wrapper::-webkit-scrollbar {
  display: none;
}

.svg-inner {
  display: inline-block;
  pointer-events: auto;
  transition: transform 0.08s ease-out;
}

.svg-inner svg {
  display: block;
  max-width: none;
  height: auto;
}
</style>
