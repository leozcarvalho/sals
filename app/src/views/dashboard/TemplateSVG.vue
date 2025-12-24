<script setup>
import { ref, onMounted, computed } from "vue";
import { ApiClient } from "../../services/genericApi";
const dashboardApi = new ApiClient("/dashboard/svg-data");

const data = ref([]);
const selectedShed = ref({});

onMounted(async () => {
  try {
    const res = await dashboardApi.getList();
    data.value = res.data || [];
    selectedShed.value = data.value[0] || {};
  } catch (err) {
    console.error("Erro ao carregar dados do dashboard:", err);
  }
});

const selectShed = (shed) => {
  selectedShed.value = shed;
}
const xSpace = ref(40); // 42.711

const svgWidth = computed(() => {
  const rooms = selectedShed.value?.rooms?.length || 0;
  return Math.max(297, 297 * rooms);
});

const calculateOffset = (index) => {
  if (!selectedShed.value?.rooms) return 0;

  // Soma as larguras de todos os galpões anteriores
  let offset = 0;
  for (let i = 0; i < index; i++) {
    const prevRoom = selectedShed.value.rooms[i];
    const stallsCount = prevRoom?.stalls?.length || 1;
    offset += stallsCount * xSpace.value + 80; // 80 = margem entre galpões
  }
  return offset;
};

// Lógica de arrasto
const svgContainer = ref(null);
const isDragging = ref(false);
const start = ref({ x: 0, y: 0 });
const scroll = ref({ left: 0, top: 0 });


const startDrag = (e) => {
  isDragging.value = true;
  svgContainer.value.style.cursor = "grabbing";
  start.value = { x: e.clientX, y: e.clientY };
  scroll.value = {
    left: svgContainer.value.scrollLeft,
    top: svgContainer.value.scrollTop,
  };
  svgContainer.value.setPointerCapture(e.pointerId);
};

const onDrag = (e) => {
  if (!isDragging.value) return;
  const dx = e.clientX - start.value.x;
  const dy = e.clientY - start.value.y;
  svgContainer.value.scrollLeft = scroll.value.left - dx;
  svgContainer.value.scrollTop = scroll.value.top - dy;
};

const endDrag = (e) => {
  if (!isDragging.value) return;
  isDragging.value = false;
  svgContainer.value.style.cursor = "grab";
  svgContainer.value.releasePointerCapture(e.pointerId);
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
    <svg xmlns="http://www.w3.org/2000/svg" :width="svgWidth + 'mm'" height="210mm" version="1.0"
      style="shape-rendering:geometricPrecision; text-rendering:geometricPrecision; image-rendering:optimizeQuality; fill-rule:evenodd; clip-rule:evenodd"
      :viewBox="`0 0 ${297 * (selectedShed.rooms?.length || 1)} 210`" xmlns:xlink="http://www.w3.org/1999/xlink"
      xmlns:xodm="http://www.corel.com/coreldraw/odm/2003">
      <g id="Telas_x0020_01">
        <metadata id="CorelCorpID_0Corel-Layer" />
        <g v-for="(room, index) in selectedShed.rooms" :key="room.id"
          :transform="`translate(${calculateOffset(index)}, 0)`">
          <rect id="base_x0020_tela" class="fil0" x="-0.0053" y="0.0713" width="297" height="210" />
          <g transform="matrix(0.736619 0 0 1 -98.0574 -65.5104)">
            <text x="148.5" y="105" class="fil1 fnt0">{{ room.entrance_pin_name }}</text>
          </g>
          <rect :class="room.entrance_pin_active ? 'fil2' : 'fil5'" transform="matrix(0.686594 -0.932088 0.735643 0.998674 16.1292 47.3146)" width="6.5647"
            height="6.127" />
          <line class="fil3 str1" x1="24.6819" y1="47.3146" x2="42" y2="47.3146" />
          <g v-for="(baia, index) in room.baias" :key="index" :transform="`translate(${xSpace * index}, 0)`">
            <line v-if="index > 0" class="fil3 str1" x1="0" y1="47.3146" x2="50" y2="47.3146" />
            <line class="fil3 str1" x1="42.5" y1="63.6316" x2="42.5" y2="47.3146" />
            <rect class="fil2" transform="matrix(0.686594 -0.932088 0.735643 0.998674 38.2038 69.7505)" width="6.5647"
              height="6.127" />
            <g transform="matrix(2.64845E-14 -1 0.736619 2.64845E-14 -27.5315 238.769)">
              <text x="148.5" y="105" class="fil1 fnt0">{{ baia.name }}</text>
            </g>
            <line class="fil3 str1" x1="42.5" y1="92.1864" x2="42.5" y2="75.8694" />
            <rect class="fil4" transform="matrix(2.73022E-14 -1.39947 1.60357 5.76552E-14 35.9911 116.662)"
              width="17.4892" height="7.4954" />
            <g transform="matrix(2.64845E-14 -1 0.736619 2.64845E-14 -32.9155 264.47)">
              <text x="148.5" y="105" class="fil1 fnt0">C</text>
              <text x="155.1511" y="105" class="fil1 fnt0">1</text>
            </g>
            <line class="fil3 str1" x1="35.9911" y1="132.6582" x2="35.9911" y2="116.3411" />
            <g transform="matrix(2.64845E-14 -1 0.736619 2.64845E-14 -36.7599 282.362)">
              <text x="137.2348" y="105" class="fil1 fnt0">B</text>
              <text x="143.3778" y="105" class="fil1 fnt0">1</text>
            </g>
            <g transform="matrix(2.64845E-14 -1 0.736619 2.64845E-14 -28.8196 282.362)">
              <text x="137.2348" y="105" class="fil1 fnt0">B</text>
              <text x="143.3778" y="105" class="fil1 fnt0">2</text>
            </g>
            <line class="fil3 str1" x1="48.0105" y1="132.9789" x2="48.0105" y2="116.6619" />
            <line class="fil3 str1" x1="35.9911" y1="167.0871" x2="35.9911" y2="150.77" />
            <g transform="matrix(2.64845E-14 -1 0.736619 2.64845E-14 -36.7599 316.791)">
              <text x="137.2348" y="105" class="fil1 fnt0">0S</text>
            </g>
            <g transform="matrix(2.64845E-14 -1 0.736619 2.64845E-14 -28.8196 316.791)">
              <text x="137.2348" y="105" class="fil1 fnt0">0S</text>
            </g>
            <line class="fil3 str1" x1="48.0105" y1="167.4079" x2="48.0105" y2="151.0908" />
          </g>
          <rect class="fil3 str2" x="33.6964" y="39.8088" :width="(room.stalls?.length || 1) * xSpace"
            height="155.0117" />
          <g transform="matrix(0.736619 0 0 1 -75.7625 99.811)">
            <text x="148.5" y="105" class="fil1 fnt0">{{ room.name }}</text>
          </g>
        </g>
        <!-- GALPOES BOTOES -->
        <g v-for="(shed, index) in data" :key="shed.id" @click="selectShed(shed)" style="cursor: pointer;">
          <!-- largura: 30.0486 / espaçamento: 5 -->
          <rect :class="shed.id === selectedShed.id ? 'fil2' : 'fil5'" :x="4.7763 + index * (30.0486 + 5)" y="5.6734"
            width="30.0486" height="16.317" />

          <!-- texto centralizado -->
          <text :x="4.7763 + index * (30.0486 + 5) + 15.0243" y="16" text-anchor="middle" class="fnt1 fil6">
            {{ shed.name }}
          </text>
        </g>
      </g>
    </svg>
  </div>
</template>

<style scoped>
@font-face {
  font-family: "Arial";
  font-variant: normal;
  font-style: normal;
  font-weight: bold;
  src: url("#FontID1") format(svg);
}

@font-face {
  font-family: "Arial";
  font-variant: normal;
  font-style: normal;
  font-weight: normal;
  src: url("#FontID0") format(svg);
}

.str1 {
  stroke: #006EC7;
  stroke-miterlimit: 22.9256;
}

.str0 {
  stroke: #373435;
  stroke-width: 0.2;
  stroke-miterlimit: 22.9256;
}

.str2 {
  stroke: #828585;
  stroke-width: 0.2;
  stroke-miterlimit: 22.9256;
}

.fil3 {
  fill: none;
}

.fil6 {
  fill: #FEFEFE;
}

.fil1 {
  fill: #373435;
}

.fil0 {
  fill: #F0F0F0;
}

.fil7 {
  fill: #3F69B0;
}

.fil2 {
  fill: #00B394;
}

.fil4 {
  fill: #F5E39E;
}

.fil5 {
  fill: #D61C38;
}

.fnt0 {
  font-weight: normal;
  font-size: 9.2099px;
  font-family: 'Arial';
}

.fnt1 {
  font-weight: bold;
  font-size: 9.2099px;
  font-family: 'Arial';
}

.svg-wrapper {
  width: 100%;
  height: 100vh; /* garante altura da tela inteira */
  overflow: scroll; /* precisa permitir rolagem */
  scrollbar-width: none; /* esconde barras no Firefox */
  -ms-overflow-style: none; /* IE e Edge antigos */
  cursor: grab;
}

.svg-wrapper::-webkit-scrollbar {
  display: none; /* esconde barras no Chrome/Safari */
}

.svg-wrapper:active {
  cursor: grabbing;
}
</style>