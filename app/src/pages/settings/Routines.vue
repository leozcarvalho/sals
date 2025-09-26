<script setup>
import { reactive, ref } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";
import BaseModalForm from "../../components/BaseModalForm.vue";
import { required, minValue } from "@vuelidate/validators";

const prioritiesApi = new ApiClient("/healthcheck-priorities");

const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Nível", field: "level" },
  { name: "Intervalo (segundos)", field: "interval_seconds" },
]);

const prioritySelected = ref(null);

const onPrioritySaved = () => {
  baseList.value.refresh();
  prioritySelected.value = null;
};

const modalForm = ref(null);
</script>

<template>
  <BaseModalForm 
    ref="modalForm" 
    v-model="prioritySelected" 
    :fields="[
      { name: 'name', label: 'Nome', type: 'text', rules: 'required' },
      { name: 'interval_milliseconds', label: 'Intervalo (milissegundos)', type: 'number', rules: 'required|minValue:1' }
    ]" 
    :api="prioritiesApi" 
    @saved="onPrioritySaved" 
    @close="prioritySelected = null" 
  />
  <BaseList 
    ref="baseList" 
    :title="'Prioridades de Healthcheck'" 
    :api="prioritiesApi" 
    :cols="cols" 
    @create="modalForm.openModal(true)"
    @edit="prioritySelected = $event; modalForm.openModal()"
  />
</template>
