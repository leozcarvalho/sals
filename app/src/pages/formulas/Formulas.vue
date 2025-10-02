<script setup>
import { ref, reactive } from "vue";
import BaseList from "../../components/BaseList.vue";
import { ApiClient } from "../../services/genericApi";

const formulasApi = new ApiClient("/formulas");
const baseList = ref(null);

const cols = reactive([
  { name: "#", field: "id" },
  { name: "Nome", field: "name" },
  { name: "Descrição", field: "description" },
  { name: "% Água", field: "water_percentage" },
  { name: "Tempo de Agitação (s)", field: "stirring_time" },
]);
</script>

<template>
  <BaseList ref="baseList" :title="'Fórmulas'" :api="formulasApi" :cols="cols" :can-edit="false" :can-create="false">
  <template #extra-actions>
    <button class="btn btn-lg btn-success" @click="$router.push({ name: 'formula-form'})" title="Adicionar fórmula">
      <i class="fa fa-plus"></i>
    </button>
  </template>
  <template #row-actions="{ row }">
    <button  class="btn btn-lg btn-warning" @click="$router.push({ name: 'formula-form', params: { id: row.id } })">
      <i class="fa fa-pencil"></i>
    </button>
  </template>
</BaseList>
</template>
