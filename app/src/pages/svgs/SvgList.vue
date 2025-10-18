<script setup>
import { ref, reactive, watch } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

const svgsApi = new ApiClient("/svgs");

const baseList = ref(null);
const modalForm = ref(null);
const svgSelected = ref(null);
const svgPreview = ref("");

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Sessão", field: "owner_type" },
]);

const ownerOptions = [
  { label: "Galpão", value: "sheds" },
  { label: "Cozinha", value: "kitchens" },
  { label: "Placa", value: "hardware-devices" },
];


const onSvgSaved = () => {
  baseList.value.refresh();
  svgSelected.value = null;
};

const showSvgPreviewModal = (svg) => {
  svgPreview.value = svg;
  let modal = new bootstrap.Modal(document.getElementById("modal-svg"));
  modal.show();
};

const ownerIdOptions = ref([]);
const fetchOwnerOptions = async (ownerType) => {
  if (!ownerType) return;
  const api = new ApiClient(`/${ownerType}`);
  const res = await api.getList();
  ownerIdOptions.value = (res.data.items || []).map(item => ({ label: item.name, value: item.id }) );
};

</script>

<template>
  <BaseModalForm
    ref="modalForm"
    v-model="svgSelected"
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'owner_type', label: 'Sessão', slot: 'owner_type', rules: 'required' },
      { name: 'owner_id', label: 'Item', type: 'select', slot: 'owner_id', rules: 'required' },
      { name: 'content', label: 'SVG', slot: 'content' }
    ]"
    :api="svgsApi"
    @saved="onSvgSaved"
    @close="svgSelected = null"
    @edit="fetchOwnerOptions(svgSelected.owner_type)"
  >
    <template #owner_type="{ model }">
      <select
        class="form-select"
        v-model="model.owner_type"
        @change="fetchOwnerOptions(model.owner_type)"
      >
        <option value="" disabled>Selecione o tipo</option>
        <option v-for="option in ownerOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>
    </template>
    <template #owner_id="{ model }">
      <select
        class="form-select"
        v-model="model.owner_id"
        :disabled="!model.owner_type"
      >
        <option value="" disabled>Selecione o item</option>
        <option v-for="option in ownerIdOptions" :key="option.value" :value="option.value">
          {{ option.label }}
        </option>
      </select>
    </template>
    <template #content="{ model }">
      <div class="flex flex-col gap-2">
        <div v-if="model.content" class="flex items-center gap-2">
          <button type="button" class="btn btn-sm btn-primary ms-2" @click="showSvgPreviewModal(model.content)">
            Mostrar
          </button>
          <button type="button" class="btn btn-sm btn-secondary ms-2" @click="model.content = null">
            Trocar
          </button>
        </div>
        <div v-else>
          <input
            type="file"
            class="form-control"
            accept=".svg"
            @change="async (e) => {
              const file = e.target.files[0];
              if (!file) return;
              const text = await file.text();
              model.content = text;
            }"
          />
        </div>
      </div>
      <div class="modal fade" id="modal-svg">
        <div class="modal-dialog">
          <div class="text-center">
            <div v-html="svgPreview" class="w-full max-h-[80vh] overflow-scroll"></div>
          </div>
        </div>
      </div>
    </template>
  </BaseModalForm>

  <BaseList
    ref="baseList"
    :title="'SVGs'"
    :api="svgsApi"
    :cols="cols"
    @create="modalForm.openModal(true)"
    @edit="svgSelected = $event; modalForm.openModal()"
  >
    <template #cell-owner_type="{ row }">
      <span>{{ ownerOptions.find(option => option.value === row.owner_type)?.label }} - {{ row.owner_name }}</span>
    </template>
    <template #row-actions="{ row }">
      <button
        class="btn btn-lg btn-primary text-white"
        @click="$router.push({ name: 'svg-config', params: { id: row.id } })"
      >
        <i class="fa fa-cog"></i>
      </button>
    </template>
  </BaseList>
</template>
