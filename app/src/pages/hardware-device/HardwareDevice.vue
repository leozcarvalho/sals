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
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Template", field: "connection_template_id", formatter: (value, row) => row.connection_template.name },
  { name: "Tipo", field: "hardware_kind_id", formatter: (value, row) => row.hardware_kind.kind },
  { name: "Tipo de Pino", field: "point_type_id", formatter: (value, row) => `${row.point_type.kind} (${row.point_type.points_quantity})` },
]);

const hardwareDeviceSelected = ref(null);

const onHardwareDeviceSaved = () => {
  baseList.value.refresh();
  hardwareDeviceSelected.value = null;
};

const modalForm = ref(null);

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
    { name: 'hardware_kind_id', label: 'Tipo', type: 'select', options: hardwareKindsOptions, rules: 'required' },
    { name: 'point_type_id', label: 'Point Type', type: 'select', options: hardwarePointTypesOptions, rules: 'required' },
    { name: 'svg_template', label: 'SVG Template', slot: 'svg_template' }
  ]" :api="hardwareDevicesApi" @saved="onHardwareDeviceSaved" @close="hardwareDeviceSelected = null">
    <template #svg_template="{ model }">
      <div class="flex flex-col gap-2">
        <div v-if="model.svg_template" class="flex items-center gap-2">
          <button type="button" class="btn btn-sm btn-primary ms-2" @click="showSvgPreviewModal(model.svg_template)">
            Mostrar
          </button>
          <button type="button" class="btn btn-sm btn-secondary ms-2" @click="model.svg_template = null">
            Trocar
          </button>
        </div>
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
    @create="modalForm.openModal(true)"
    @edit="hardwareDeviceSelected = $event; modalForm.openModal()"
  />
</template>
