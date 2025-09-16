<script setup>
import { reactive, ref } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

const hardwareConnectionTemplatesApi = new ApiClient("/hardware-connection-templates");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Template URL", field: "template_url" },
]);

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
    @create="modalForm.openModal(true)"
    @edit="hardwareConnectionTemplateSelected = $event; modalForm.openModal()"
  />
</template>
