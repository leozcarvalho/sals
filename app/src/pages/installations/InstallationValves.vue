<script setup>
import { ref, onMounted, computed, nextTick } from "vue";
import { useRoute } from "vue-router";
import { InstallationClient } from "../../services/installationsApi";
import { handleApiToast } from "../../components/toast";
import Loader from "@/components/Loader.vue";

const route = useRoute();
const installationApi = new InstallationClient();

const loader = ref(false);
const installation = ref(null);

const deviceId = ref(route.params.id);

const updatePins = async () => {
  loader.value.loaderOn();
  const payload = installation.value.pins.map(pin => ({
    id: pin.id,
    name: pin.name,
  }));
  const res = await installationApi.updateDevicePins(installation.value.id, payload);
  if (res.success) refresh();
  handleApiToast(res, 'Válvulas atualizadas com sucesso');
  loader.value.loaderOff();
};

const refresh = async () => {
  loader.value.loaderOn();
  const response = await installationApi.get(deviceId.value);
  installation.value = response.data;
  loader.value.loaderOff();
};

onMounted(async () => {
  await refresh();
});
</script>

<template>
  <Loader ref="loader" />
  <div class="content">
    <BaseBlock title="Válvulas">
      <div v-for="(valve, index) in installation?.pins" :key="index" class="row g-2 align-items-start mb-2">
        <!-- Produto -->
        <div class="col-2">
          <input v-model="valve.arbitrary_name" type="text"  class="form-control"
            disabled
           />
        </div>

        <!-- % Produto -->
        <div class="col-auto">
          <input v-model="valve.name" type="text"  class="form-control"
            placeholder="Alias: ex: Válvula 1"
           />
        </div>
      </div>
      <button class="btn btn-primary mb-4 btn-lg" @click="updatePins">Salvar</button>
    </BaseBlock>
  </div>
</template>
