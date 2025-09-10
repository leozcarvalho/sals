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
const svgPreview = ref("");
const showSvgPreviewModal = (svg) => {
  svgPreview.value = svg;
  let modal = new bootstrap.Modal(
    document.getElementById("modal-svg")
  );
  modal.show();
};
</script>

<template>
  <BaseModalForm ref="modalForm" v-model="hardwareDeviceSelected" :fields="[
    { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
    { name: 'connection_template_id', label: 'Template', type: 'select', options: connectionTemplatesOptions, rules: 'required' },
    { name: 'hardware_kind_id', label: 'Kind', type: 'select', options: hardwareKindsOptions, rules: 'required' },
    { name: 'point_type_id', label: 'Point Type', type: 'select', options: hardwarePointTypesOptions, rules: 'required' },
    { name: 'svg_template', label: 'SVG Template', slot: 'svg_template' }
  ]" :api="hardwareDevicesApi" @saved="onHardwareDeviceSaved" @close="hardwareDeviceSelected = null">
    <template #svg_template="{ model }">
      <div class="flex flex-col gap-2">
        <div v-if="model.svg_template" class="flex items-center gap-2">
          <!-- Botão para abrir modal -->
          <button type="button" class="btn btn-sm btn-primary ms-2" @click="showSvgPreviewModal(model.svg_template)">
            Mostrar
          </button>

          <!-- Botão para trocar -->
          <button type="button" class="btn btn-sm btn-secondary ms-2" @click="model.svg_template = null">
            Trocar
          </button>
        </div>

        <!-- Input de upload -->
        <div v-else>
          <input type="file" class="form-control" accept=".svg" @change="async (e) => {
            const file = e.target.files[0];
            if (!file) return;
            const text = await file.text();
            model.svg_template = text;
          }" />
        </div>
      </div>
      <div class="modal fade" id="modal-svg">
        <div class="modal-dialog">
          <div class="text-center">
            <div v-html="svgPreview" class="w-full max-h-[80vh] overflow-auto"></div>
          </div>
        </div>
      </div>
    </template>
  </BaseModalForm>

  <BaseList ref="baseList" :title="'Dispositivos de Hardware'" :api="hardwareDevicesApi" :cols="cols"
    :can-create="false" :can-edit="false" :filter="filter" v-model:filter="filter">
    <!-- Botão Criar -->
    <template #extra-actions>
      <button type="button" class="btn btn-sm btn-success ms-2" @click="modalForm.openModal(true)">
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
      <button class="btn btn-sm btn-warning text-white" @click="hardwareDeviceSelected = row; modalForm.openModal()">
        <mdicon name="circle-edit-outline" />
      </button>
    </template>
  </BaseList>
</template>
