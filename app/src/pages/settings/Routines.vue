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

const filter = reactive({});

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
      { name: 'level', label: 'Nível', type: 'number', rules: 'required|minValue:1' },
      { name: 'interval_seconds', label: 'Intervalo (segundos)', type: 'number', rules: 'required|minValue:1' }
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

    <!-- Ações de linha -->
    <template #row-actions="{ row }">
      <button 
        class="btn btn-sm btn-warning text-white" 
        @click="prioritySelected = row; modalForm.openModal()"
      >
        <mdicon name="circle-edit-outline" />
      </button>
    </template>
  </BaseList>
</template>
