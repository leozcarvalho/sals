<script setup>
import { reactive, ref, onMounted } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

const hardwareDevicesApi = new ApiClient("/hardware-devices");
const hardwareConnectionTemplatesApi = new ApiClient("/hardware-connection-templates");
const hardwareKindsApi = new ApiClient("/hardware-kinds");
const hardwarePointTypesApi = new ApiClient("/hardware-point-types");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id", sort: "" },
  { name: "Nome", field: "name", sort: "" },
  { name: "Template", field: "connection_template_id", sort: "" },
  { name: "Tipo", field: "hardware_kind_id", sort: "" },
  { name: "Tipo de Pino", field: "point_type_id", sort: "" },
]);

const filter = reactive({
  name: null,
  connection_template_id: null,
  hardware_kind_id: null,
  point_type_id: null,
});

const hardwareDeviceSelected = ref(null);

const onHardwareDeviceSaved = () => {
  baseList.value.refresh();
  hardwareDeviceSelected.value = null;
};

const modalForm = ref(null);
const openModal = () => {
  modalForm.value.openModal();
};

// opções para selects
const connectionTemplatesOptions = ref([]);
const hardwareKindsOptions = ref([]);
const hardwarePointTypesOptions = ref([]);

onMounted(async () => {
  const res = await hardwareConnectionTemplatesApi.getList()
  connectionTemplatesOptions.value = res.data.items.map(t => ({
    label: t.name,
    value: t.id,
  }));
  const res2 = await hardwareKindsApi.getList()
  hardwareKindsOptions.value = res2.data.items.map(k => ({
    label: k.kind,
    value: k.id,
  }));
  const res3 = await hardwarePointTypesApi.getList()
  hardwarePointTypesOptions.value = res3.data.items.map(p => ({
    label: `${p.points_quantity} (${p.kind})`,
    value: p.id,
  }));
});
</script>

<template>
  <BaseModalForm 
    ref="modalForm" 
    v-model="hardwareDeviceSelected" 
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'connection_template_id', label: 'Template', type: 'select', options: connectionTemplatesOptions, rules: 'required' },
      { name: 'hardware_kind_id', label: 'Kind', type: 'select', options: hardwareKindsOptions, rules: 'required' },
      { name: 'point_type_id', label: 'Point Type', type: 'select', options: hardwarePointTypesOptions, rules: 'required' }
    ]" 
    :api="hardwareDevicesApi" 
    @saved="onHardwareDeviceSaved" 
    @close="hardwareDeviceSelected = null" 
  />

  <BaseList 
    ref="baseList" 
    :title="'Dispositivos de Hardware'" 
    :api="hardwareDevicesApi" 
    :cols="cols" 
    :exportable="false" 
    :can-create="false"
    :can-edit="false" 
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
        <div class="col-md-3">
          <label class="form-label">Nome</label>
          <input v-model="filter.name" class="form-control" />
        </div>
        <div class="col-md-3">
          <label class="form-label">Template</label>
          <select v-model="filter.connection_template_id" class="form-control">
            <option :value="null">Todos</option>
            <option v-for="opt in connectionTemplatesOptions" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>
        <div class="col-md-3">
          <label class="form-label">Kind</label>
          <select v-model="filter.hardware_kind_id" class="form-control">
            <option :value="null">Todos</option>
            <option v-for="opt in hardwareKindsOptions" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>
        <div class="col-md-3">
          <label class="form-label">Point Type</label>
          <select v-model="filter.point_type_id" class="form-control">
            <option :value="null">Todos</option>
            <option v-for="opt in hardwarePointTypesOptions" :key="opt.value" :value="opt.value">
              {{ opt.label }}
            </option>
          </select>
        </div>
        <div class="text-center mt-4">
          <button type="button" class="btn btn-success" @click="baseList.refresh()">FILTRAR</button>
        </div>
      </div>
    </template>
    <template #cell-connection_template_id="{ row }">
      <span>
        {{ row.connection_template.name }}
      </span>
    </template>
    <template #cell-hardware_kind_id="{ row }">
      <span>
        {{ row.hardware_kind.kind }}
      </span>
    </template>
    <template #cell-point_type_id="{ row }">
      <span>
        {{ row.point_type.kind }} ({{ row.point_type.points_quantity }})
      </span>
    </template>
    <!-- Ações de linha -->
    <template #row-actions="{ row }">
      <button 
        class="btn btn-sm btn-warning text-white" 
        @click="hardwareDeviceSelected = row; openModal()"
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
