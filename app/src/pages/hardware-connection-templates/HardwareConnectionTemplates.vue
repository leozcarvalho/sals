<script setup>
import { reactive, ref } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";
import { required } from "@vuelidate/validators";

const hardwareConnectionTemplatesApi = new ApiClient("/hardware-connection-templates");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id", sort: "" },
  { name: "Nome", field: "name", sort: "" },
  { name: "Template URL", field: "template_url", sort: "" },
]);

const filter = reactive({
  name: null,
  template_url: null,
});

const hardwareConnectionTemplateSelected = ref(null);

const onHardwareConnectionTemplateSaved = () => {
  baseList.value.refresh();
  hardwareConnectionTemplateSelected.value = null;
};

const modalForm = ref(null);
</script>

<template>
  <BaseModalForm 
    ref="modalForm" 
    v-model="hardwareConnectionTemplateSelected" 
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'template_url', label: 'Template URL', type: 'text', rules: 'required' }
    ]" 
    :api="hardwareConnectionTemplatesApi" 
    @saved="onHardwareConnectionTemplateSaved" 
    @close="hardwareConnectionTemplateSelected = null" 
  />

  <BaseList 
    ref="baseList" 
    :title="'Templates de Conexão de Hardware'" 
    :api="hardwareConnectionTemplatesApi" 
    :cols="cols" 
    :exportable="false" 
    :can-create="false"
    :can-edit="false" 
    :filter="filter" 
    v-model:filter="filter"
  >
    <!-- Botão Criar -->
    <template #extra-actions>
      <button type="button" class="btn btn-sm btn-success ms-2" @click="modalForm.openModal(true)">
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
          <label class="form-label">Template URL</label>
          <input v-model="filter.template_url" class="form-control" />
        </div>
        <div class="text-center mt-4">
          <button type="button" class="btn btn-success" @click="baseList.refresh()">FILTRAR</button>
        </div>
      </div>
    </template>

    <!-- Ações de linha -->
    <template #row-actions="{ row }">
      <button 
        class="btn btn-sm btn-warning text-white" 
        @click="hardwareConnectionTemplateSelected = row; modalForm.openModal()"
      >
        <mdicon name="circle-edit-outline" />
      </button>
    </template>
  </BaseList>
</template>
