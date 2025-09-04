<script setup>
import { ref, onMounted, computed, nextTick } from "vue";
import { useRoute } from "vue-router";
import { AccountDeviceClient } from "../../services/accountDeviceApi";
import { ApiClient } from "../../services/genericApi";
import { handleApiToast } from "../../components/toast";
import { formatDateBrl } from "@/helpers/formatters";
import Loader from "@/components/Loader.vue";
import deviceSvgFile from './pro-mini-nologo.svg?url';
const svgContent = ref("");

const route = useRoute();
const accountDeviceApi = new AccountDeviceClient();
const pinsApi = new ApiClient("/device-pins");

const loader = ref(false);
const accountDevice = ref(null);

const deviceId = ref(route.query.id || null);
const selectedPin = ref(null);
const modalForm = ref(null);

const openModal = () => {
  modalForm.value.openModal();
};

const togglePin = async (pin) => {
  loader.value.loaderOn();
  const res = await accountDeviceApi.togglePin(accountDevice.value.id, pin.id);
  handleApiToast(res, `${pin.name} ${pin.is_active ? "desligado" : "ativado"} com sucesso`);
  await refresh();
  loader.value.loaderOff();
};

const statusClass = computed(() => {
  return accountDevice.value?.is_online ? "text-success" : "text-danger";
});

const healthCheck = async () => {
  loader.value.loaderOn();
  const res = await accountDeviceApi.healthCheck(accountDevice.value.id);
  handleApiToast(res, "Conexão verificada com sucesso");
  await refresh();
  loader.value.loaderOff();
};

const restartDevice = async () => {
  loader.value.loaderOn();
  const res = await accountDeviceApi.restart(accountDevice.value.id);
  handleApiToast(res, "Dispositivo reiniciado com sucesso");
  await refresh();
  loader.value.loaderOff();
};

const refresh = async () => {
  loader.value.loaderOn();
  if (!deviceId.value) return;
  const response = await accountDeviceApi.get(deviceId.value);
  accountDevice.value = response.data;
  fillPins();
  loader.value.loaderOff();
};

function fillPins() {
  const svgEl = document.querySelector('#uploaded-svg');
  if (!svgEl) return;

  accountDevice.value.pins.forEach(pin => {
    const el = svgEl.querySelector(`[id="${pin.svg_region_id}"]`);
    if (el) {
      el.style.fill = pin.is_active ? pin.activation_color || "green" : "red";
      el.style.cursor = "pointer";
      el.onclick = () => togglePin(pin);
    }
  });
}


onMounted(async () => {
  fetch(deviceSvgFile)
    .then(res => res.text())
    .then(svg => {
      svgContent.value = svg;
    });
  await refresh();
});
</script>

<template>
  <Loader ref="loader" />
  <div class="device-page container mt-5">
    <h2>Placa: {{ accountDevice?.name }}</h2>
    <p>IP: {{ accountDevice?.ip_address }}</p>

    <div class="text-center">
      <div v-if="svgContent" v-html="svgContent" id="uploaded-svg"></div>
    </div>
    <!-- Status do dispositivo com botões -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div>
        <span class="me-3">
          Último acesso: {{ formatDateBrl(accountDevice?.last_seen) || '-' }}
        </span>
        <span :class="statusClass">
          {{ accountDevice?.is_online ? "Online" : "Offline" }}
        </span>
      </div>
      <div>
        <button class="btn btn-info btn-sm me-2" title="Verificar conexão" @click="healthCheck">
          <mdicon name="check" />
        </button>
        <button class="btn btn-warning btn-sm" title="Reiniciar dispositivo" @click="restartDevice">
          <mdicon name="restart" />
        </button>
      </div>
    </div>

    <!-- Pinos -->
    <div class="pins-layout mt-4">
      <h4>Pinos</h4>
      <div class="row">
        <div v-for="pin in accountDevice?.pins" :key="pin.id" class="col-6 col-md-2 mb-3 text-center position-relative">
          <button class="btn w-100 position-relative" :class="pin.is_active ? 'btn-success' : 'btn-danger'"
            @click="togglePin(pin)">
            {{ pin.name }}
          </button>
        </div>
      </div>
    </div>
    <div class="my-4">
      <small>
        Valor binário: {{ accountDevice?.binary_value }} | Valor decimal: {{ accountDevice?.decimal_value }}
      </small>
    </div>
  </div>
</template>

<style scoped>
</style>
