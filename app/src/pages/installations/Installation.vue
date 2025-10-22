<script setup>
import { ref, onMounted, computed, nextTick } from "vue";
import { useRoute } from "vue-router";
import { InstallationClient } from "../../services/installationsApi";
import { SVGClient } from "../../services/svg";
import SVGPanel from "../../components/SVGPanel.vue";
import { handleApiToast } from "../../components/toast";
import { formatDateBrl } from "@/helpers/formatters";
import Loader from "@/components/Loader.vue";

const route = useRoute();
const installationApi = new InstallationClient();
const svgApi = new SVGClient();

const loader = ref(false);
const installation = ref(null);

const deviceId = ref(route.query.id || null);

const togglePin = async (pin) => {
  loader.value.loaderOn();
  const res = await installationApi.togglePin(installation.value.id, pin.id);
  handleApiToast(res, `${pin.name} ${pin.is_active ? "desligado" : "ativado"} com sucesso`);
  await refresh();
  loader.value.loaderOff();
};

const statusClass = computed(() => {
  return installation.value?.is_online ? "text-success" : "text-danger";
});

const healthCheck = async () => {
  loader.value.loaderOn();
  const res = await installationApi.healthCheck(installation.value.id);
  handleApiToast(res, "Conexão verificada com sucesso");
  await refresh();
  loader.value.loaderOff();
};

const restartDevice = async () => {
  loader.value.loaderOn();
  const res = await installationApi.restart(installation.value.id);
  handleApiToast(res, "Dispositivo reiniciado com sucesso");
  await refresh();
  loader.value.loaderOff();
};

const svgId = ref(null);
const loadSvg = async () => {
  const res = await svgApi.getOwnerSvgId("installations", installation.value.id);
  svgId.value = res.data?.svg_id || null;
  if (svgId.value) {
    await nextTick();
    if (SVGPanelRef.value) {
      await SVGPanelRef.value.refresh();
    }
  }
};

const SVGPanelRef = ref(null);
const refresh = async () => {
  loader.value.loaderOn();
  if (!deviceId.value) return;
  const response = await installationApi.get(deviceId.value);
  installation.value = response.data;
  await loadSvg();
  loader.value.loaderOff();
};

onMounted(async () => {
  await refresh();
});
</script>

<template>
  <Loader ref="loader" />
  <div class="device-page container mt-5">
    <h2>Placa: {{ installation?.name }}</h2>
    <p>IP: {{ installation?.ip_address }}</p>

    <div class="text-center" v-if="svgId">
      <SVGPanel ref="SVGPanelRef" :svgId="svgId" />
    </div>
    <!-- Status do dispositivo com botões -->
    <div class="d-flex justify-content-between align-items-center mb-3">
      <div>
        <span class="me-3">
          Último acesso: {{ formatDateBrl(installation?.last_seen) || '-' }}
        </span>
        <span :class="statusClass">
          {{ installation?.is_online ? "Online" : "Offline" }}
        </span>
      </div>
      <div>
        <button class="btn btn-info btn-lg me-2" title="Verificar conexão" @click="healthCheck">
          <mdicon name="check" />
        </button>
        <button class="btn btn-warning btn-lg" title="Reiniciar dispositivo" @click="restartDevice">
          <mdicon name="restart" />
        </button>
      </div>
    </div>
    <div class="pins-layout mt-4">
      <h4>Válvulas</h4>
      <div class="row">
        <div v-for="pin in installation?.pins" :key="pin.id" class="col-6 col-md-2 mb-3 text-center position-relative">
          <button class="btn w-100 position-relative" :class="pin.is_active ? 'btn-success' : 'btn-danger'"
            @click="togglePin(pin)">
            {{ pin.name }}
          </button>
        </div>
      </div>
    </div>
    <div class="my-4">
      <small>
        Valor binário: {{ installation?.binary_value }} | Valor decimal: {{ installation?.decimal_value }}
      </small>
    </div>
  </div>
</template>

<style scoped>
</style>
