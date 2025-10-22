<script setup>
import { ref, onMounted, nextTick, defineExpose } from "vue";
import { ApiClient } from "../services/genericApi";
import { SVGClient } from "../services/svg";
import { DevicePinsClient } from "../services/devicePins";
import SVGView from "../components/SVGView.vue";
import { handleApiToast } from "../components/toast";

const props = defineProps({
  svgId: { type: Number },
});
const svgsApi = new SVGClient();
const devicePinsApi = new DevicePinsClient();

const associateOptions = ref([]);
const variablesOptions = ref([]);
const loadOptions = async (svgId) => {
  const res = await svgsApi.options(svgId);
  associateOptions.value = res.data.options || [];
  variablesOptions.value = res.data.variables || [];
};

const togglePin = async (pinId) => {
  const res = await devicePinsApi.togglePin(pinId);
  if (res.success) {
    handleApiToast(res, `Pino alternado com sucesso`);
    refresh();
  }
};

const fillSvg = () => {
  const svgEl = document.querySelector("#uploaded-svg");
  if (!svgEl) return;

  // 🔹 Percorre todas as regiões que têm data-type
  const regions = svgEl.querySelectorAll("[data-type]");
  regions.forEach(region => {
    const type = region.getAttribute("data-type");

    if (type === "pin") {
      const pinId = region.getAttribute("data-value");
      if (!pinId) return;

      const pin = associateOptions.value.find(p => p.value.toString() === pinId.toString());
      if (!pin) return;

      region.style.fill = pin.is_active ? "#00ff00" : "#ff0000";
      region.style.cursor = "pointer";
      region.ondblclick = () => togglePin(pinId);
    }

    if (type === "text") {
      const variableName = region.getAttribute("data-value");
      if (!variableName) return;
      const variable = variablesOptions.value.find(v => v.key === variableName);
      if (!variable) return;
      region.textContent = variable.value || "";
    }
  });
};

const svgData = ref(null);
const fetchSvg = async () => {
 const res = await svgsApi.get(props.svgId);
  svgData.value = res.data || {};
  if (svgData.value) {
    await loadOptions(svgData.value.id); // <-- adicione o await aqui
  }
}

const refresh = async () => {
  await fetchSvg();
  await nextTick();
  fillSvg();
};

defineExpose({
  refresh,
});
const svgView = ref(null);
</script>

<template>
  <div v-if="svgData">
    <SVGView ref="svgView" :svg="svgData.content" />
  </div>
</template>
