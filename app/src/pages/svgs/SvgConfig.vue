<script setup>
import { ref, onMounted, nextTick } from "vue";
import { useRoute } from "vue-router";
import { ApiClient } from "../../services/genericApi";
import { handleApiToast } from "../../components/toast";
import Loader from "@/components/Loader.vue";
import SVGView from "../../components/SVGView.vue";

const route = useRoute();
const svgsApi = new ApiClient("/svgs");

const loader = ref(false);
const svg = ref(null);
const svgView = ref(null);
const svgId = ref(route.params.id);
const selectedPin = ref(null);
const selectedRegion = ref(null); // última região clicada no SVG

/** Helpers */
const setStroke = (el, active = false) => {
  el.style.stroke = active ? "yellow" : null;
  el.style.strokeWidth = active ? "2px" : null;
};

const refresh = async () => {
  if (!svgId.value) return;
  loader.value.loaderOn();
  const response = await svgsApi.get(svgId.value);
  svg.value = response.data;
  //nextTick(fillPins);
  loader.value.loaderOff();
};

const associateRegion = async () => {
  if (!selectedRegion.value) return;
  loader.value.loaderOn();
  selectedPin.value.svg_region_id = selectedRegion.value.id;
  handleApiToast(res, `Pino ${selectedPin.value.name} associado à região com sucesso`);
  resetSelection();
  await refresh();
  loader.value.loaderOff();
};

/** SVG */
function enableRegionSelection() {
  const svgEl = document.querySelector('#uploaded-svg');
  if (!svgEl) return;

  svgEl.addEventListener("dblclick", (e) => {
    if (e.target.tagName.toLowerCase() === "svg") return;

    if (selectedRegion.value) setStroke(selectedRegion.value, false);
    console.log("selected region", e.target.outerHTML);
    selectedRegion.value = e.target;
    setStroke(e.target, true);

    document.querySelector("#associate-section")?.scrollIntoView({ behavior: "smooth", block: "start" });
  });
}

function fillPins() {
  const svgEl = document.querySelector('#uploaded-svg');
  if (!svgEl || !installation.value) return;

  installation.value.pins.forEach(pin => {
    const el = svgEl.querySelector(`[id="${pin.svg_region_id}"]`);
    const btn = document.querySelector(`#pin-btn-${pin.id}`);

    if (el) {
      // define a cor do SVG
      el.style.fill = pin.activation_color || (pin.svg_region_id ? '#4CAF50' : '#E74C3C');
      el.style.cursor = "pointer";

      // --- Hover na região do SVG ---
      el.onmouseenter = () => {
        setStroke(el, true);
        if (btn) btn.classList.add("btn-outline-warning");
      };
      el.onmouseleave = () => {
        setStroke(el, false);
        if (btn) btn.classList.remove("btn-outline-warning");
      };
    }

    if (btn && el) {
      // --- Hover no botão ---
      btn.onmouseenter = () => setStroke(el, true);
      btn.onmouseleave = () => setStroke(el, false);
    }
  });
}

const resetSelection = () => {
  if (selectedRegion.value) setStroke(selectedRegion.value, false);
  selectedPin.value = null;
  selectedRegion.value = null;
};

onMounted(async () => {
  await refresh();
  nextTick(() => {
    //fillPins();
    enableRegionSelection();
  });
});

const pinStyle = (pin) => {
  if (selectedRegion.value && pin.svg_region_id) {
    return { backgroundColor: "#6c757d" }; // cinza no modo associação
  }

  // Se tiver activation_color cadastrado, usa ele
  if (pin.activation_color && pin.svg_region_id) {
    return { backgroundColor: pin.activation_color };
  }

  // fallback: verde se associado, vermelho se não
  return { backgroundColor: pin.svg_region_id ? "#4CAF50" : "#E74C3C" };
};

function getRegionPreviewHtml(element, width = 200, height = 100) {
  if (!element) return "";

  // calcula bbox do elemento para ajustar o viewBox
  const bbox = element.getBBox();
  const padding = 5; // opcional, deixa espaço em volta

  const viewBox = `${bbox.x - padding} ${bbox.y - padding} ${bbox.width + 2 * padding} ${bbox.height + 2 * padding}`;

  return `<svg width="${width}" height="${height}" viewBox="${viewBox}" xmlns="http://www.w3.org/2000/svg">
            ${element.outerHTML}
          </svg>`;
}
</script>

<template>
  <div class="modal fade" id="modal-confirm" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">Confirmar Ação</div>
        <div class="modal-body">
          Associar {{ selectedPin?.name }} à região selecionada?
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal" @click="resetSelection">
            Cancelar
          </button>
          <button class="btn btn-danger" data-bs-dismiss="modal" @click="associatePin">
            Confirmar
          </button>
        </div>
      </div>
    </div>
  </div>

  <Loader ref="loader" />

  <div class="device-page container mt-5 text-center">
    <h2>Configurar SVG</h2>
    <SVGView ref="svgView" :svg="svg?.content" />
  </div>
  <div class="container mt-4" id="associate-section">
    <div v-if="selectedRegion">
      <h3>Associar Região</h3>
      <div class="bg-light border p-3 container text-center">
        <div v-html="getRegionPreviewHtml(selectedRegion)"></div>
      </div>
    </div>
  </div>
</template>

<style scoped>
</style>
