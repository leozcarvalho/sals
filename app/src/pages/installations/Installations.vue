<script setup>
import { reactive, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

const router = useRouter();

const installationsApi = new ApiClient("/installations");
const hardwareDevicesApi = new ApiClient("/hardware-devices");
const routinesApi = new ApiClient("/healthcheck-priorities");

const baseList = ref(null);

const cols = reactive([
  { name: "Nome", field: "name" },
  { name: "Placa", field: "device_id", formatter: (value, row) => row.device.name },
]);

const installationsSelected = ref(null);

const oninstallationsSaved = () => {
  baseList.value.refresh();
  installationsSelected.value = null;
};

const modalForm = ref(null);

const devicesOptions = ref([]);
const healthCheckOptions = ref([]);

onMounted(async () => {
  const res2 = await hardwareDevicesApi.getList()
  devicesOptions.value = res2.data.items.map(d => ({
    label: d.name,
    value: d.id,
  }));
  const res3 = await routinesApi.getList()
  healthCheckOptions.value = res3.data.items.map(d => ({
    label: d.name,
    value: d.id,
  }));
});
</script>

<template>
  <BaseModalForm 
    ref="modalForm" 
    v-model="installationsSelected" 
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'ip_address', label: 'IP Address', type: 'text', rules: 'required' },
      { name: 'device_id', label: 'Dispositivo', type: 'select', options: devicesOptions, rules: 'required' },
      { name: 'healthcheck_priority_id', label: 'Rotina de Verificação', type: 'select', options: healthCheckOptions }
    ]" 
    :api="installationsApi" 
    @saved="oninstallationsSaved" 
    @close="installationsSelected = null" 
  />

  <BaseList 
    ref="baseList" 
    :title="'Instalações'" 
    :api="installationsApi" 
    :cols="cols" 
    :can-delete="false"
    @create="modalForm.openModal(true)"
    @edit="installationsSelected = $event; modalForm.openModal()"
  >
    <template #row-actions="{ row }">
      <button 
        class="btn btn-lg btn-success text-white" 
        @click="router.push({ name: 'installation', query: { id: row.id } })"
        title="Painel de controle"
      >
        <mdicon name="tune-vertical-variant" />
      </button>
    </template>
  </BaseList>
</template>
