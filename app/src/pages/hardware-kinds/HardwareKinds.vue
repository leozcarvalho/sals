<script setup>
import { reactive, ref } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";
import { required } from "@vuelidate/validators";

const hardwareKindsApi = new ApiClient("/hardware-kinds");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id", sort: "" },
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
      { name: 'kind', label: 'Tipo', type: 'text', rules: 'required' }
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
    :filter="filter" 
    v-model:filter="filter"
    @create="modalForm.openModal(true)"
    @edit="hardwareKindSelected = $event; modalForm.openModal()"
  />
</template>
