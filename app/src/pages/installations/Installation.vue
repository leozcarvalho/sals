<script setup>
import { ref, onMounted, computed, nextTick } from "vue";
import { useRoute } from "vue-router";
import { InstallationClient } from "../../services/installationsApi";
import { SVGClient } from "../../services/svg";
import { DevicePinsClient } from "../../services/devicePins";
import SVGPanel from "../../components/SVGPanel.vue";
import { handleApiToast } from "../../components/toast";
import { formatDateBrl } from "@/helpers/formatters";
import Loader from "@/components/Loader.vue";

const route = useRoute();
const installationApi = new InstallationClient();
const svgApi = new SVGClient();
const devicePinsApi = new DevicePinsClient();

const loader = ref(false);
const installation = ref(null);

const deviceId = ref(route.query.id);

const statusClass = computed(() => {
  return installation.value?.is_online ? "text-success" : "text-danger";
});

const actionValues = ref({
  weight: null,
});
const execAction = async (action, payload) => {
  loader.value.loaderOn();
  const res = await installationApi.execAction(installation.value.id, action, payload);
  handleApiToast(res, res.data);
  loader.value.loaderOff();
  await refresh();
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
  const response = await installationApi.get(deviceId.value);
  installation.value = response.data;
  await loadSvg();
  loader.value.loaderOff();
};

const togglePin = async (pinId) => {
  loader.value.loaderOn();
  const res = await devicePinsApi.togglePin(pinId);
  if (res.success) {
    handleApiToast(res, `Pino alternado com sucesso`);
    await refresh();
  }
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
        <button class="btn btn-info btn-lg me-2" title="Verificar conexão" @click="execAction('healthcheck')">
          <mdicon name="check" />
        </button>
        <button class="btn btn-warning btn-lg me-2" title="Reiniciar dispositivo" @click="execAction('restart')">
          <mdicon name="restart" />
        </button>
        <button v-if="installation?.hardware_kind === 'input'" class="btn btn-primary btn-lg me-2" title="Tarar balança"
          @click="execAction('tare')">
          Tarar
        </button>
        <div class="input-group mt-3" v-if="installation?.hardware_kind === 'input'">
          <input v-model="actionValues.weight" type="number" step="0.01" class="form-control" placeholder="Peso" />
          <button class="input-group-text btn-primary" @click="execAction('calibrate', actionValues)">Calibrar</button>
        </div>
      </div>
    </div>
    <div class="pins-layout mt-4">
      <h4>Válvulas</h4>
      <div class="row">
        <div v-for="pin in installation?.pins" :key="pin.id" class="col-6 col-md-2 mb-3 text-center position-relative">
          <button class="btn w-100 position-relative" :class="pin.is_active ? 'btn-success' : 'btn-danger'"
            :disabled="installation.hardware_kind === 'input'" @click="togglePin(pin.id)">
            {{ pin.name }}
          </button>
        </div>
      </div>
    </div>
    <div class="my-4" v-if="installation?.hardware_kind === 'output'">
      <small>
        Valor binário: {{ installation?.binary_value }} | Valor decimal: {{ installation?.decimal_value }}
      </small>
    </div>
  </div>
</template>

<style scoped></style>
