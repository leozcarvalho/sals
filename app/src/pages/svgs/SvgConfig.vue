<script setup>
import { ref, onMounted, nextTick } from "vue";
import { useRoute } from "vue-router";
import { SVGClient } from "../../services/svg";
//import { ApiClient } from "../../services/genericApi";
import { handleApiToast } from "../../components/toast";
import Loader from "@/components/Loader.vue";
import SVGView from "../../components/SVGView.vue";

const route = useRoute();
const svgsApi = new SVGClient();
//const svgRegionApi = new ApiClient("/svg-regions");

const loader = ref(false);
const svg = ref(null);
const svgView = ref(null);
const svgId = ref(route.params.id);
const selectedRegion = ref(null);
const selectedOption = ref(null);

const associateOptions = ref([]);
const loadOptions = async () => {
  if (!svgId.value) return;
  const res = await svgsApi.options(svgId.value);
  associateOptions.value = res.data || [];
};

const variablesOptions = ref([]);
const loadVariables = async () => {
  if (!svgId.value) return;
  const res = await svgsApi.variables(svgId.value);
  variablesOptions.value = res.data || [];
};

const setStroke = (el, active = false) => {
  el.style.stroke = active ? "yellow" : null;
  el.style.strokeWidth = active ? "0.5px" : null;
};

const refresh = async () => {
  if (!svgId.value) return;
  loader.value.loaderOn();
  const response = await svgsApi.get(svgId.value);
  svg.value = response.data;
  loader.value.loaderOff();
};

const associateRegion = async () => {
  if (!selectedRegion.value) return;
  loader.value.loaderOn();
  selectedRegion.value.setAttribute("data-type", selectedRegion.value.kind);
  selectedRegion.value.setAttribute("data-value", selectedOption.value || "");
  if (selectedRegion.value.kind === "text") selectedRegion.value.textContent = selectedOption.value || "";

  // --- 🔹 Remove visualização temporária do stroke antes de salvar ---
  const originalStroke = selectedRegion.value.style.stroke;
  const originalStrokeWidth = selectedRegion.value.style.strokeWidth;
  setStroke(selectedRegion.value, false);

  // atualiza conteúdo do SVG completo
  const svgEl = document.querySelector("#uploaded-svg");
  if (svgEl) {
    svg.value.content = svgEl.outerHTML;
    const res = await svgsApi.update(svgId.value, svg.value);
    if (res.success) {
      handleApiToast(res, `Região atualizada e salva com sucesso`);
      await refresh();
    }
  }

  // 🔹 Restaura o contorno visual (apenas visual, não salvo)
  selectedRegion.value.style.stroke = originalStroke;
  selectedRegion.value.style.strokeWidth = originalStrokeWidth;

  resetSelection();
  loader.value.loaderOff();
};

const enableRegionSelection = () => {
  const svgEl = document.querySelector('#uploaded-svg');
  if (!svgEl) return;

  svgEl.addEventListener("dblclick", (e) => {
    if (e.target.tagName.toLowerCase() === "svg") return;

    if (selectedRegion.value) setStroke(selectedRegion.value, false);
    selectedRegion.value = e.target;

    if (e.target.tagName.toLowerCase() === "text") selectedRegion.value.kind = "text";
    else selectedRegion.value.kind = "pin";

    setStroke(e.target, true);

    const modalEl = document.getElementById('modal-associate');
    if (modalEl) {
      const modal = new bootstrap.Modal(modalEl);
      modal.show();
    }
  });
}

const resetSelection = () => {
  if (selectedRegion.value) setStroke(selectedRegion.value, false);
  selectedRegion.value = null;
};

onMounted(async () => {
  await refresh();
  await loadOptions();
  await loadVariables();
  nextTick(() => {
    enableRegionSelection();
  });
});

const getRegionPreviewHtml = (element, width = 200, height = 100) => {
  if (!element) return "";
  const bbox = element.getBBox();
  const padding = 5;
  const viewBox = `${bbox.x - padding} ${bbox.y - padding} ${bbox.width + 2 * padding} ${bbox.height + 2 * padding}`;

  // 🔹 Clona o elemento para evitar modificar o original
  const clone = element.cloneNode(true);
  clone.style.stroke = "none";
  clone.style.strokeWidth = "0";

  return `<svg width="${width}" height="${height}" viewBox="${viewBox}" xmlns="http://www.w3.org/2000/svg">
            ${clone.outerHTML}
          </svg>`;
};
</script>

<template>
  <div class="modal fade" id="modal-associate" tabindex="-1">
    <div class="modal-dialog">
      <div class="modal-content">
        <div class="modal-header">Associar Região</div>
        <div class="modal-body">
          <div class="bg-white border p-3 container text-center">
            <div v-html="getRegionPreviewHtml(selectedRegion)"></div>
          </div>
          <div class="mt-3">
            <label for="associate-option" class="form-label">Associar à:</label>
            <select id="associate-option" class="form-select" v-model="selectedOption" v-if="selectedRegion?.kind === 'text'">
              <option value="" disabled>Selecione uma opção</option>
              <option v-for="option in variablesOptions" :key="option.key" :value="option.key">
                {{ option.label }}
              </option>
            </select>
            <select id="associate-option" class="form-select" v-model="selectedOption" v-else>
              <option value="" disabled>Selecione uma opção</option>
              <option v-for="option in associateOptions" :key="option.value" :value="option.value">
                {{ option.label }}
              </option>
            </select>
          </div>
        </div>
        <div class="modal-footer">
          <button class="btn btn-secondary" data-bs-dismiss="modal">
            Cancelar
          </button>
          <button class="btn btn-danger" data-bs-dismiss="modal" @click="associateRegion">
            Confirmar
          </button>
        </div>
      </div>
    </div>
  </div>
  <Loader ref="loader" />
  <div class="container mt-5 text-center">
    <h2>Configurar SVG</h2>
    <SVGView ref="svgView" :svg="svg?.content" />
  </div>
</template>

<style scoped></style>
