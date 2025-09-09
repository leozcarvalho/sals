<script setup>
import { ref, onMounted, nextTick } from "vue";
import { useRoute } from "vue-router";
import { InstallationClient } from "../../services/installationsApi";
import { ApiClient } from "../../services/genericApi";
import { handleApiToast } from "../../components/toast";
import Loader from "@/components/Loader.vue";
import BaseModalForm from "../../components/BaseModalForm.vue";

const svgContent = ref("");
const route = useRoute();
const installationApi = new InstallationClient();
const pinsApi = new ApiClient("/device-pins");

const loader = ref(false);
const installation = ref(null);
const deviceId = ref(route.query.id || null);
const selectedPin = ref(null);
const modalForm = ref(null);
const selectedRegion = ref(null); // última região clicada no SVG

/** Helpers */
const setStroke = (el, active = false) => {
  el.style.stroke = active ? "yellow" : null;
  el.style.strokeWidth = active ? "3px" : null;
};

/** API */
const refresh = async () => {
  if (!deviceId.value) return;
  loader.value.loaderOn();
  const response = await installationApi.get(deviceId.value);
  installation.value = response.data;
  svgContent.value = installation.value?.device?.svg_template || "";
  nextTick(fillPins);
  loader.value.loaderOff();
};

const associatePin = async () => {
  if (!selectedPin.value || !selectedRegion.value) return;
  loader.value.loaderOn();
  selectedPin.value.svg_region_id = selectedRegion.value.id;
  const res = await pinsApi.update(selectedPin.value.id, selectedPin.value);
  handleApiToast(res, `Pino ${selectedPin.value.name} associado à região com sucesso`);
  resetSelection();
  await refresh();
  loader.value.loaderOff();
};

/** SVG */
function enableRegionSelection() {
  const svgEl = document.querySelector('#uploaded-svg');
  if (!svgEl) return;

  svgEl.addEventListener("click", (e) => {
    if (e.target.tagName.toLowerCase() === "svg") return;

    if (selectedRegion.value) setStroke(selectedRegion.value, false);

    selectedRegion.value = e.target;
    setStroke(e.target, true);

    document.querySelector("#pins-section")?.scrollIntoView({ behavior: "smooth", block: "start" });
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


/** UI Actions */
const openModal = () => modalForm.value.openModal();

const execPinAction = (pin) => {
  selectedPin.value = pin;
  if (selectedRegion.value) {
    new bootstrap.Modal(document.getElementById("modal-confirm")).show();
  } else {
    openModal();
  }
};

const resetSelection = () => {
  if (selectedRegion.value) setStroke(selectedRegion.value, false);
  selectedPin.value = null;
  selectedRegion.value = null;
};


/** Lifecycle */
onMounted(async () => {
  await refresh();
  nextTick(() => {
    fillPins();
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
</script>

<template>
  <BaseModalForm :api="pinsApi" ref="modalForm" v-model="selectedPin"
    :fields="[{ name: 'name', label: 'Nome', type: 'text', rules: 'required' },{ name: 'activation_color', label: 'Cor', slot: 'color-picker' }]"
    @close="selectedPin = null" @saved="refresh">
    <template #color-picker="{ field, model }">
      <input type="color" v-model="model[field.name]" class="form-control form-control-color" />
    </template>
  </BaseModalForm>

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

  <div class="device-page container mt-5">
    <h2>Configurar pinos de {{ installation?.name }}</h2>

    <div class="text-center">
      <div v-if="svgContent" v-html="svgContent" id="uploaded-svg"></div>
    </div>

    <div class="pins-layout mt-4" id="pins-section">
      <h4>Pinos</h4>
      <h4 class="animated fadeIn" v-if="selectedRegion">Selecionar pino disponível</h4>
      <div class="row">
        <div v-for="pin in installation?.pins" :key="pin.id" class="col-6 col-md-2 mb-3 text-center position-relative">
          <button
            :id="`pin-btn-${pin.id}`"
            class="pin-box btn w-100 position-relative"
            :style="pinStyle(pin)"
            @click="execPinAction(pin)"
            :disabled="selectedRegion && pin.svg_region_id"
          >
            {{ pin.name }}
          </button>
        </div>
      </div>
    </div>
  </div>
</template>

<style scoped>
.pin-box {
  cursor: pointer;
  min-height: 50px;
  font-weight: bold;
}

.pin-menu {
  top: 100%;
  left: 50%;
  transform: translateX(-50%);
  z-index: 1000;
  min-width: 160px;
  background-color: #171e28;
}

@media (max-width: 768px) {
  .pin-box {
    min-height: 60px;
    font-size: 1rem;
  }

  .pin-menu {
    left: 0;
    right: 0;
    transform: none;
    min-width: unset;
  }
}
</style>
