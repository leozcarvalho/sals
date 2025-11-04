<script setup>
import { reactive, ref } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

const hardwareKindsApi = new ApiClient("/hardware-kinds");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id", sort: "" },
  { name: "Nome", field: "name", sort: "" },
  { name: "Tipo", field: "kind", sort: "" },
]);

const hardwareKindSelected = ref(null);

const onHardwareKindSaved = () => {
  baseList.value.refresh();
  hardwareKindSelected.value = null;
};

const modalForm = ref(null);
</script>

<template>
  <BaseModalForm 
    ref="modalForm" 
    v-model="hardwareKindSelected" 
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'kind', label: 'Tipo', type: 'select', options: [{ label: 'Saída', value: 'output' }, { label: 'Entrada', value: 'input' }], rules: 'required' }
    ]" 
    :api="hardwareKindsApi" 
    @saved="onHardwareKindSaved" 
    @close="hardwareKindSelected = null" 
  />

  <BaseList 
    ref="baseList" 
    :title="'Tipos de Hardware'" 
    :api="hardwareKindsApi" 
    :cols="cols" 
    @create="modalForm.openModal(true)"
    @edit="hardwareKindSelected = $event; modalForm.openModal()"
  />
</template>
