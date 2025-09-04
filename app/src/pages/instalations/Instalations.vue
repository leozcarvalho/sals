<script setup>
import { reactive, ref, onMounted } from "vue";
import { useRouter } from "vue-router";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

const router = useRouter();

const instalationsApi = new ApiClient("/instalations");
const hardwareDevicesApi = new ApiClient("/hardware-devices");

const baseList = ref(null);

const cols = reactive([
  { name: "Nome", field: "name", sort: "" },
  { name: "Placa", field: "device_id", sort: "" },
]);

const filter = reactive({
  name: null,
  device_id: null,
});

const instalationsSelected = ref(null);

const onInstalationsSaved = () => {
  baseList.value.refresh();
  instalationsSelected.value = null;
};

const modalForm = ref(null);
const openModal = () => {
  modalForm.value.openModal();
};

// opções selects
const devicesOptions = ref([]);

onMounted(async () => {
  const res2 = await hardwareDevicesApi.getList()
  devicesOptions.value = res2.data.items.map(d => ({
    label: d.name,
    value: d.id,
  }));
});
</script>

<template>
  <BaseModalForm 
    ref="modalForm" 
    v-model="instalationsSelected" 
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'ip_address', label: 'IP Address', type: 'text', rules: 'required' },
      { name: 'device_id', label: 'Dispositivo', type: 'select', options: devicesOptions, rules: 'required' }
    ]" 
    :api="instalationsApi" 
    @saved="onInstalationsSaved" 
    @close="instalationsSelected = null" 
  />

  <BaseList 
    ref="baseList" 
    :title="'Instalações'" 
    :api="instalationsApi" 
    :cols="cols" 
    :exportable="false" 
    :can-create="false"
    :can-edit="false" 
    :can-delete="false"
    :filter="filter" 
    v-model:filter="filter"
  >
    <!-- Botão Criar -->
    <template #extra-actions>
      <button type="button" class="btn btn-sm btn-success ms-2" @click="openModal">
        <mdicon name="plus" />
      </button>
    </template>

    <!-- Filtros -->
    <template #filter>
      <div class="row px-5 py-5">
        <div class="col-md-4">
          <label class="form-label">Nome</label>
          <input v-model="filter.name" class="form-control" />
        </div>
        <div class="col-md-4">
          <label class="form-label">Dispositivo</label>
          <select v-model="filter.device_id" class="form-control">
            <option :value="null">Todos</option>
            <option v-for="opt in devicesOptions" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>
        <div class="text-center mt-4">
          <button type="button" class="btn btn-success" @click="baseList.refresh()">FILTRAR</button>
        </div>
      </div>
    </template>

    <template #cell-account_id="{ row }">
      <span>
        {{ row.account.name }}
      </span>
    </template>
    <template #cell-device_id="{ row }">
      <span>
        {{ row.device.name }}
      </span>
    </template>

    <!-- Ações de linha -->
    <template #row-actions="{ row }">
      <button 
        class="btn btn-sm btn-success text-white" 
        @click="router.push({ name: 'instalation', query: { id: row.id } })"
        title="Painel de controle"
      >
        <mdicon name="tune-vertical-variant" />
      </button>
      <button 
        class="btn btn-sm btn-primary text-white" 
        @click="router.push({ name: 'instalation-pin-config', query: { id: row.id } })"
        title="Configurar Pinos"
      >
        <mdicon name="cog-outline" />
      </button>
      <button 
        class="btn btn-sm btn-warning text-white" 
        @click="instalationsSelected = row; openModal()"
      >
        <mdicon name="circle-edit-outline" />
      </button>
    </template>
  </BaseList>
</template>

<style lang="scss" scoped>
@import url('../../assets/scss/custom/_tablestyle.scss');

.last-read {
  cursor: pointer;
}
</style>
