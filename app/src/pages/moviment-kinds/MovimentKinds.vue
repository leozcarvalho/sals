<script setup>
import { reactive, ref } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";

const movimentKindsApi = new ApiClient("/moviment-kinds");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id", sort: "" },
  { name: "Tipo", field: "kind", sort: "" },
  { name: "Código", field: "code", sort: "" },
]);

const movimentKindSelected = ref(null);

const onMovimentKindSaved = () => {
  baseList.value.refresh();
  movimentKindSelected.value = null;
};

const modalForm = ref(null);
const movimentOptions = ref([
  { label: "ENTRADA", value: "ENTRADA" },
  { label: "SAIDA", value: "SAIDA" },
  { label: "TRANSFERENCIA", value: "TRANSFERENCIA" },
]);
</script>

<template>
  <BaseModalForm 
    ref="modalForm"
    v-model="movimentKindSelected"
    :fields="[
      { name: 'kind', label: 'Tipo', type: 'select', options: movimentOptions, rules: 'required' },
      { name: 'code', label: 'Código', type: 'text' }
    ]"
    :api="movimentKindsApi"
    @saved="onMovimentKindSaved"
    @close="movimentKindSelected = null"
  />

  <BaseList 
    ref="baseList"
    :title="'Tipos de Movimentação'"
    :api="movimentKindsApi"
    :cols="cols"
    @create="modalForm.openModal(true)"
    @edit="movimentKindSelected = $event; modalForm.openModal()"
  />
</template>
